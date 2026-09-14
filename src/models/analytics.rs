use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize, sqlx::FromRow)]
pub struct CropYieldSummary {
    pub crop: String,
    pub average_yield_tons: f64,
    pub total_records: i64,
}

#[derive(Debug, Clone, Serialize, Deserialize, sqlx::FromRow)]
pub struct ProfitSummary {
    pub crop: String,
    pub total_revenue: f64,
    pub total_cost: f64,
    pub total_profit: f64,
    pub average_profit_per_record: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize, sqlx::FromRow)]
pub struct RevenueSummary {
    pub state: String,
    pub total_revenue: f64,
    pub total_records: i64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QualityReport {
    pub dataset_id: Uuid,
    pub total_records: i64,
    pub missing_yield: i64,
    pub missing_rainfall: i64,
    pub negative_profit: i64,
    pub duplicate_farmer_ids: i64,
    pub quality_score: f64,
}
