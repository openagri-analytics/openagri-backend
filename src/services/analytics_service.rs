use sqlx::PgPool;
use uuid::Uuid;

use crate::{
    models::analytics::{CropYieldSummary, ProfitSummary, QualityReport, RevenueSummary},
    AppResult,
};

pub async fn yield_by_crop(pool: &PgPool) -> AppResult<Vec<CropYieldSummary>> {
    let rows = sqlx::query_as::<_, CropYieldSummary>(
        r#"
        SELECT
            crop,
            ROUND(AVG(yield_tons)::numeric, 2)::float8 AS average_yield_tons,
            COUNT(*) AS total_records
        FROM agriculture_records
        WHERE yield_tons IS NOT NULL
        GROUP BY crop
        ORDER BY average_yield_tons DESC
        "#,
    )
    .fetch_all(pool)
    .await?;
    Ok(rows)
}

pub async fn profit_by_crop(pool: &PgPool) -> AppResult<Vec<ProfitSummary>> {
    let rows = sqlx::query_as::<_, ProfitSummary>(
        r#"
        SELECT
            crop,
            COALESCE(SUM(revenue), 0)                           AS total_revenue,
            COALESCE(SUM(production_cost), 0)                   AS total_cost,
            COALESCE(SUM(profit), 0)                            AS total_profit,
            ROUND(COALESCE(AVG(profit), 0)::numeric, 2)::float8 AS average_profit_per_record
        FROM agriculture_records
        GROUP BY crop
        ORDER BY total_profit DESC
        "#,
    )
    .fetch_all(pool)
    .await?;
    Ok(rows)
}

pub async fn revenue_by_region(pool: &PgPool) -> AppResult<Vec<RevenueSummary>> {
    let rows = sqlx::query_as::<_, RevenueSummary>(
        r#"
        SELECT
            state,
            COALESCE(SUM(revenue), 0) AS total_revenue,
            COUNT(*) AS total_records
        FROM agriculture_records
        GROUP BY state
        ORDER BY total_revenue DESC
        "#,
    )
    .fetch_all(pool)
    .await?;
    Ok(rows)
}

pub async fn distinct_crops(pool: &PgPool) -> AppResult<Vec<String>> {
    let rows: Vec<(String,)> =
        sqlx::query_as("SELECT DISTINCT crop FROM agriculture_records ORDER BY crop")
            .fetch_all(pool)
            .await?;
    Ok(rows.into_iter().map(|(c,)| c).collect())
}

pub async fn quality_report(pool: &PgPool, dataset_id: Uuid) -> AppResult<QualityReport> {
    let (total,): (i64,) =
        sqlx::query_as("SELECT COUNT(*) FROM agriculture_records WHERE dataset_id = $1")
            .bind(dataset_id)
            .fetch_one(pool)
            .await?;

    let (missing_yield,): (i64,) = sqlx::query_as(
        "SELECT COUNT(*) FROM agriculture_records WHERE dataset_id=$1 AND yield_tons IS NULL",
    )
    .bind(dataset_id)
    .fetch_one(pool)
    .await?;

    let (missing_rainfall,): (i64,) = sqlx::query_as(
        "SELECT COUNT(*) FROM agriculture_records WHERE dataset_id=$1 AND rainfall_mm IS NULL",
    )
    .bind(dataset_id)
    .fetch_one(pool)
    .await?;

    let (negative_profit,): (i64,) = sqlx::query_as(
        "SELECT COUNT(*) FROM agriculture_records WHERE dataset_id=$1 AND profit < 0",
    )
    .bind(dataset_id)
    .fetch_one(pool)
    .await?;

    let (duplicate_farmer_ids,): (i64,) = sqlx::query_as(
        r#"SELECT COUNT(*) FROM (
               SELECT farmer_id FROM agriculture_records WHERE dataset_id=$1
               GROUP BY farmer_id HAVING COUNT(*) > 1
           ) d"#,
    )
    .bind(dataset_id)
    .fetch_one(pool)
    .await?;

    let issues =
        (missing_yield + missing_rainfall + negative_profit + duplicate_farmer_ids) as f64;
    let quality_score =
        ((1.0 - issues / total.max(1) as f64) * 100.0).clamp(0.0, 100.0);
    let quality_score = (quality_score * 10.0).round() / 10.0;

    Ok(QualityReport {
        dataset_id,
        total_records: total,
        missing_yield,
        missing_rainfall,
        negative_profit,
        duplicate_farmer_ids,
        quality_score,
    })
}
