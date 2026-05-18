-- =============================================================================
-- 02_staging_profit_view.sql — Order-level staging view with profit metrics
-- =============================================================================
-- Depends on: ecommerce_orders (loaded via 01_load_duckdb.sql)
--
-- Creates stg_orders_profit with calculated fields used by all analysis queries.
-- Discount bands match scripts/analyze_profit_leaks.py (pd.cut bins).
-- =============================================================================

CREATE OR REPLACE VIEW stg_orders_profit AS
SELECT
    -- Original columns
    order_id,
    customer_id,
    product_category,
    region,
    order_date,
    revenue,
    cost,
    discount,

    -- Profit metrics
    revenue - cost AS profit,
    (revenue - cost) / NULLIF(revenue, 0) AS profit_margin,

    -- Discount band (aligned with Python: bins (-0.001, 0.05], (0.05, 0.10], …, (0.30, 0.45])
    CASE
        WHEN discount <= 0.05  THEN '0-5%'
        WHEN discount <= 0.10  THEN '5-10%'
        WHEN discount <= 0.15  THEN '10-15%'
        WHEN discount <= 0.20  THEN '15-20%'
        WHEN discount <= 0.25  THEN '20-25%'
        WHEN discount <= 0.30  THEN '25-30%'
        WHEN discount <= 0.45  THEN '30-45%'
        ELSE 'Out of range'
    END AS discount_band,

    -- Month grain for time-series analysis (Tableau, monthly trend query)
    DATE_TRUNC('month', order_date) AS order_month

FROM ecommerce_orders;
