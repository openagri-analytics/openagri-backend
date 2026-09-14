-- OpenAgri Analytics — PostgreSQL Schema
-- Matches the SQLx migration in the backend (mirrors 0001_initial_schema.sql)
-- Use this file for manual setup, analytics tooling, or standalone SQL work.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ── Datasets ──────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS datasets (
    id            UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    name          TEXT        NOT NULL,
    description   TEXT,
    record_count  BIGINT,
    file_hash     TEXT,
    source        TEXT,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ── Agricultural Records ──────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS agriculture_records (
    id                  UUID             PRIMARY KEY DEFAULT gen_random_uuid(),
    dataset_id          UUID             NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    farmer_id           TEXT             NOT NULL,
    state               TEXT             NOT NULL,
    crop                TEXT             NOT NULL,
    farm_size_hectares  DOUBLE PRECISION NOT NULL,
    yield_tons          DOUBLE PRECISION,
    fertilizer_used     TEXT,
    irrigation          BOOLEAN          NOT NULL DEFAULT FALSE,
    rainfall_mm         DOUBLE PRECISION,
    market_price        DOUBLE PRECISION,
    production_cost     DOUBLE PRECISION,
    revenue             DOUBLE PRECISION,
    profit              DOUBLE PRECISION,
    harvest_date        DATE,
    created_at          TIMESTAMPTZ      NOT NULL DEFAULT NOW()
);

-- ── Indexes ───────────────────────────────────────────────────────────────────

CREATE INDEX IF NOT EXISTS idx_agri_records_dataset  ON agriculture_records(dataset_id);
CREATE INDEX IF NOT EXISTS idx_agri_records_crop     ON agriculture_records(crop);
CREATE INDEX IF NOT EXISTS idx_agri_records_state    ON agriculture_records(state);
CREATE INDEX IF NOT EXISTS idx_agri_records_harvest  ON agriculture_records(harvest_date);
