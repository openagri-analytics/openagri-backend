use sqlx::PgPool;
use uuid::Uuid;

use crate::{
    error::AppError,
    models::dataset::{CreateDataset, Dataset},
    AppResult,
};

pub async fn list_all(pool: &PgPool) -> AppResult<Vec<Dataset>> {
    let rows = sqlx::query_as::<_, Dataset>(
        "SELECT id, name, description, record_count, file_hash, source, created_at, updated_at
         FROM datasets ORDER BY created_at DESC",
    )
    .fetch_all(pool)
    .await?;
    Ok(rows)
}

pub async fn find_by_id(pool: &PgPool, id: Uuid) -> AppResult<Dataset> {
    sqlx::query_as::<_, Dataset>(
        "SELECT id, name, description, record_count, file_hash, source, created_at, updated_at
         FROM datasets WHERE id = $1",
    )
    .bind(id)
    .fetch_optional(pool)
    .await?
    .ok_or_else(|| AppError::NotFound(format!("Dataset {id} not found")))
}

pub async fn create(pool: &PgPool, payload: CreateDataset) -> AppResult<Dataset> {
    if payload.name.trim().is_empty() {
        return Err(AppError::BadRequest("Dataset name cannot be empty".into()));
    }
    let dataset = sqlx::query_as::<_, Dataset>(
        r#"
        INSERT INTO datasets (id, name, description, file_hash, source, created_at, updated_at)
        VALUES (gen_random_uuid(), $1, $2, $3, $4, NOW(), NOW())
        RETURNING id, name, description, record_count, file_hash, source, created_at, updated_at
        "#,
    )
    .bind(&payload.name)
    .bind(&payload.description)
    .bind(&payload.file_hash)
    .bind(&payload.source)
    .fetch_one(pool)
    .await?;
    Ok(dataset)
}

pub async fn delete(pool: &PgPool, id: Uuid) -> AppResult<()> {
    let result = sqlx::query("DELETE FROM datasets WHERE id = $1")
        .bind(id)
        .execute(pool)
        .await?;
    if result.rows_affected() == 0 {
        return Err(AppError::NotFound(format!("Dataset {id} not found")));
    }
    Ok(())
}
