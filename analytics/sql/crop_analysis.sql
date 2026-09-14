-- OpenAgri Analytics — Crop Analysis Queries
-- Run against the openagri PostgreSQL database.

-- ── 1. Average yield by crop ──────────────────────────────────────────────────
SELECT
    crop,
    ROUND(AVG(yield_tons)::numeric, 2)  AS average_yield_tons,
    MIN(yield_tons)                      AS min_yield_tons,
    MAX(yield_tons)                      AS max_yield_tons,
    COUNT(*)                             AS record_count
FROM agriculture_records
WHERE yield_tons IS NOT NULL
GROUP BY crop
ORDER BY average_yield_tons DESC;

-- ── 2. Yield by crop and state ────────────────────────────────────────────────
SELECT
    state,
    crop,
    ROUND(AVG(yield_tons)::numeric, 2) AS average_yield_tons,
    COUNT(*)                           AS record_count
FROM agriculture_records
WHERE yield_tons IS NOT NULL
GROUP BY state, crop
ORDER BY state, average_yield_tons DESC;

-- ── 3. Irrigation impact on yield ────────────────────────────────────────────
SELECT
    crop,
    irrigation,
    ROUND(AVG(yield_tons)::numeric, 2) AS average_yield_tons,
    COUNT(*)                           AS record_count
FROM agriculture_records
WHERE yield_tons IS NOT NULL
GROUP BY crop, irrigation
ORDER BY crop, irrigation;

-- ── 4. Rainfall vs yield correlation (by crop) ───────────────────────────────
SELECT
    crop,
    ROUND(AVG(rainfall_mm)::numeric, 1)  AS avg_rainfall_mm,
    ROUND(AVG(yield_tons)::numeric, 2)   AS avg_yield_tons,
    COUNT(*)                             AS record_count
FROM agriculture_records
WHERE yield_tons IS NOT NULL AND rainfall_mm IS NOT NULL
GROUP BY crop
ORDER BY avg_yield_tons DESC;

-- ── 5. Top 10 highest-yield farms ────────────────────────────────────────────
SELECT
    farmer_id,
    state,
    crop,
    yield_tons,
    farm_size_hectares,
    ROUND((yield_tons / NULLIF(farm_size_hectares, 0))::numeric, 2) AS yield_per_hectare
FROM agriculture_records
WHERE yield_tons IS NOT NULL
ORDER BY yield_tons DESC
LIMIT 10;

-- ── 6. Fertilizer usage and average yield ────────────────────────────────────
SELECT
    fertilizer_used,
    ROUND(AVG(yield_tons)::numeric, 2) AS average_yield_tons,
    COUNT(*)                           AS record_count
FROM agriculture_records
WHERE yield_tons IS NOT NULL AND fertilizer_used IS NOT NULL
GROUP BY fertilizer_used
ORDER BY average_yield_tons DESC;
