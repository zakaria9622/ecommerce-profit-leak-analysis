-- =============================================================================
-- 00_schema.sql — Raw table definition for e-commerce orders
-- =============================================================================
-- Canonical source of truth: data/ecommerce_orders.csv
--
-- Use this file to document the expected schema before loading data.
-- Run sql/01_load_duckdb.sql to populate the table from the CSV.
--
-- Do NOT use data/cleaned_dataset.csv — it may map region code NA (North America)
-- to Unknown and break regional profitability analysis.
-- =============================================================================

CREATE TABLE IF NOT EXISTS ecommerce_orders (
    order_id         VARCHAR,   -- Unique order identifier (e.g. O100001)
    customer_id      VARCHAR,   -- Customer identifier (e.g. C10001)
    product_category VARCHAR,   -- Product line (Electronics, Fashion, etc.)
    region           VARCHAR,   -- Market: NA, EU, APAC, LATAM (NA = North America)
    order_date       DATE,      -- Order date
    revenue          DOUBLE,    -- Order revenue after discount
    cost             DOUBLE,    -- Order cost
    discount         DOUBLE     -- Discount rate as decimal (0.15 = 15%)
);
