use axum::{
    extract::{Path, State},
    routing::{delete, get, post},
    Json, Router,
};
use sqlx::PgPool;
use uuid::Uuid;

use crate::{
    models::dataset::{CreateDataset, Dataset},
    services::dataset_service,
    AppResult,
};

pub fn router() -> Router<PgPool> {
    Router::new()
        .route("/datasets",     get(list_datasets).post(create_dataset))
        .route("/datasets/:id", get(get_dataset).delete(delete_dataset))
}

async fn list_datasets(State(pool): State<PgPool>) -> AppResult<Json<Vec<Dataset>>> {
    Ok(Json(dataset_service::list_all(&pool).await?))
}

async fn get_dataset(
    State(pool): State<PgPool>,
    Path(id): Path<Uuid>,
) -> AppResult<Json<Dataset>> {
    Ok(Json(dataset_service::find_by_id(&pool, id).await?))
}

async fn create_dataset(
    State(pool): State<PgPool>,
    Json(payload): Json<CreateDataset>,
) -> AppResult<Json<Dataset>> {
    Ok(Json(dataset_service::create(&pool, payload).await?))
}

async fn delete_dataset(
    State(pool): State<PgPool>,
    Path(id): Path<Uuid>,
) -> AppResult<Json<serde_json::Value>> {
    dataset_service::delete(&pool, id).await?;
    Ok(Json(serde_json::json!({ "deleted": id })))
}
