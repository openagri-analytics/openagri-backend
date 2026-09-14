use axum::{routing::get, Json, Router};
use serde_json::{json, Value};
use sqlx::PgPool;

pub fn router() -> Router<PgPool> {
    Router::new().route("/health", get(health_handler))
}

async fn health_handler() -> Json<Value> {
    Json(json!({
        "status": "ok",
        "service": "openagri-backend",
        "version": env!("CARGO_PKG_VERSION")
    }))
}
