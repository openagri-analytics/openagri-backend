-- OpenAgri Analytics — Profit Analysis Queries
-- Run against the openagri PostgreSQL database.

-- ── 1. Profit breakdown by crop ───────────────────────────────────────────────
SELECT
    crop,
    SUM(revenue)                                         AS total_revenue,
    SUM(production_cost)                                 AS total_cost,
    SUM(profit)                                          AS total_profit,
    ROUND(AVG(profit)::numeric, 2)                       AS average_profit,
    COUNT(*)                                             AS record_count
FROM agriculture_records
GROUP BY crop
ORDER BY total_profit DESC;

-- ── 2. Profit margin by crop ──────────────────────────────────────────────────
SELECT
    crop,
    ROUND(
        (SUM(profit) / NULLIF(SUM(revenue), 0) * 100)::numeric,
        1
    ) AS profit_margin_pct,
    COUNT(*) AS record_count
FROM agriculture_records
WHERE revenue > 0
GROUP BY crop
ORDER BY profit_margin_pct DESC;

-- ── 3. Profit by state ────────────────────────────────────────────────────────
SELECT
    state,
    SUM(profit)                    AS total_profit,
    ROUND(AVG(profit)::numeric, 2) AS average_profit,
    COUNT(*)                       AS record_count
FROM agriculture_records
GROUP BY state
ORDER BY total_profit DESC;

-- ── 4. Revenue vs cost comparison by crop ────────────────────────────────────
SELECT
    crop,
    ROUND(AVG(revenue)::numeric, 2)         AS avg_revenue,
    ROUND(AVG(production_cost)::numeric, 2) AS avg_cost,
    ROUND(AVG(profit)::numeric, 2)          AS avg_profit
FROM agriculture_records
GROUP BY crop
ORDER BY avg_profit DESC;

-- ── 5. Loss-making records ───────────────────────────────────────────────────
SELECT
    farmer_id,
    state,
    crop,
    revenue,
    production_cost,
    profit
FROM agriculture_records
WHERE profit < 0
ORDER BY profit ASC;

-- ── 6. Monthly profit trend ───────────────────────────────────────────────────
SELECT
    DATE_TRUNC('month', harvest_date) AS month,
    SUM(profit)                       AS total_profit,
    COUNT(*)                          AS record_count
FROM agriculture_records
WHERE harvest_date IS NOT NULL
GROUP BY month
ORDER BY month;
