use axum::{Router, http::Method};
use tower_http::cors::{Any, CorsLayer};
use tower_http::trace::TraceLayer;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

mod config;
mod db;
mod error;
mod models;
mod routes;
mod services;

pub use error::{AppError, AppResult};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // ── Logging ──────────────────────────────────────────────────────────────
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "openagri_backend=debug,tower_http=debug".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    // ── Config ───────────────────────────────────────────────────────────────
    let cfg = config::Config::from_env()?;
    tracing::info!("Starting OpenAgri backend on {}", cfg.server_addr());

    // ── Database ─────────────────────────────────────────────────────────────
    let pool = db::postgres::connect(&cfg.database_url).await?;
    db::postgres::run_migrations(&pool).await?;

    // ── CORS ─────────────────────────────────────────────────────────────────
    let cors = CorsLayer::new()
        .allow_methods([Method::GET, Method::POST, Method::DELETE, Method::PUT])
        .allow_origin(Any)
        .allow_headers(Any);

    // ── Router ───────────────────────────────────────────────────────────────
    let app = Router::new()
        .merge(routes::health::router())
        .merge(routes::datasets::router())
        .merge(routes::analytics::router())
        .with_state(pool)
        .layer(cors)
        .layer(TraceLayer::new_for_http());

    // ── Serve ────────────────────────────────────────────────────────────────
    let listener = tokio::net::TcpListener::bind(cfg.server_addr()).await?;
    tracing::info!("Listening on http://{}", cfg.server_addr());
    axum::serve(listener, app).await?;

    Ok(())
}
