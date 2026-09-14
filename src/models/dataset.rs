use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize, sqlx::FromRow)]
pub struct Dataset {
    pub id: Uuid,
    pub name: String,
    pub description: Option<String>,
    pub record_count: Option<i64>,
    pub file_hash: Option<String>,
    pub source: Option<String>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CreateDataset {
    pub name: String,
    pub description: Option<String>,
    pub source: Option<String>,
    pub file_hash: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize, sqlx::FromRow)]
pub struct AgricultureRecord {
    pub id: Uuid,
    pub dataset_id: Uuid,
    pub farmer_id: String,
    pub state: String,
    pub crop: String,
    pub farm_size_hectares: f64,
    pub yield_tons: Option<f64>,
    pub fertilizer_used: Option<String>,
    pub irrigation: bool,
    pub rainfall_mm: Option<f64>,
    pub market_price: Option<f64>,
    pub production_cost: Option<f64>,
    pub revenue: Option<f64>,
    pub profit: Option<f64>,
    pub harvest_date: Option<chrono::NaiveDate>,
}
