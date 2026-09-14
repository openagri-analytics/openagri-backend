use axum::{
    extract::{Path, State},
    routing::get,
    Json, Router,
};
use sqlx::PgPool;
use uuid::Uuid;

use crate::{
    models::analytics::{CropYieldSummary, ProfitSummary, QualityReport, RevenueSummary},
    services::analytics_service,
    AppResult,
};

pub fn router() -> Router<PgPool> {
    Router::new()
        .route("/analytics/yield",               get(yield_summary))
        .route("/analytics/profit",              get(profit_summary))
        .route("/analytics/revenue",             get(revenue_summary))
        .route("/analytics/crops",               get(crop_list))
        .route("/analytics/quality/:dataset_id", get(quality_report))
}

async fn yield_summary(State(pool): State<PgPool>) -> AppResult<Json<Vec<CropYieldSummary>>> {
    Ok(Json(analytics_service::yield_by_crop(&pool).await?))
}

async fn profit_summary(State(pool): State<PgPool>) -> AppResult<Json<Vec<ProfitSummary>>> {
    Ok(Json(analytics_service::profit_by_crop(&pool).await?))
}

async fn revenue_summary(State(pool): State<PgPool>) -> AppResult<Json<Vec<RevenueSummary>>> {
    Ok(Json(analytics_service::revenue_by_region(&pool).await?))
}

async fn crop_list(State(pool): State<PgPool>) -> AppResult<Json<Vec<String>>> {
    Ok(Json(analytics_service::distinct_crops(&pool).await?))
}

async fn quality_report(
    State(pool): State<PgPool>,
    Path(dataset_id): Path<Uuid>,
) -> AppResult<Json<QualityReport>> {
    Ok(Json(analytics_service::quality_report(&pool, dataset_id).await?))
}
