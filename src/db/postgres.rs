use anyhow::Result;
use sqlx::{postgres::PgPoolOptions, PgPool};

/// Connect to PostgreSQL and return a connection pool.
pub async fn connect(database_url: &str) -> Result<PgPool> {
    let pool = PgPoolOptions::new()
        .max_connections(10)
        .connect(database_url)
        .await?;
    Ok(pool)
}

/// Run pending SQLx migrations from the `migrations/` directory.
pub async fn run_migrations(pool: &PgPool) -> Result<()> {
    sqlx::migrate!("./migrations").run(pool).await?;
    Ok(())
}
