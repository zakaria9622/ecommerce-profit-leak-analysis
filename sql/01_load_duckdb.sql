-- =============================================================================
-- 01_load_duckdb.sql — Load canonical CSV into DuckDB
-- =============================================================================
-- Canonical source: data/ecommerce_orders.csv
--
-- Do NOT use data/cleaned_dataset.csv for SQL or Tableau.
-- That file may treat region value NA (North America) as missing and replace it
-- with Unknown, which corrupts regional KPIs.
--
-- Run from the repository root, e.g.:
--   duckdb data/profit_leak.duckdb < sql/01_load_duckdb.sql
-- Or interactively:
--   duckdb data/profit_leak.duckdb
--   .read sql/01_load_duckdb.sql
-- =============================================================================

-- Replace table on each load (idempotent refresh)
DROP TABLE IF EXISTS ecommerce_orders;

CREATE TABLE ecommerce_orders AS
SELECT
    order_id,
    customer_id,
    product_category,
    region,
    CAST(order_date AS DATE)  AS order_date,
    CAST(revenue AS DOUBLE)   AS revenue,
    CAST(cost AS DOUBLE)      AS cost,
    CAST(discount AS DOUBLE)  AS discount
FROM read_csv(
    'data/ecommerce_orders.csv',
    header   = true,
    delim    = ',',
    -- Explicit column types prevent read_csv_auto from mis-parsing region NA as NULL
    columns  = {
        order_id:         'VARCHAR',
        customer_id:      'VARCHAR',
        product_category: 'VARCHAR',
        region:           'VARCHAR',
        order_date:       'VARCHAR',
        revenue:          'DOUBLE',
        cost:             'DOUBLE',
        discount:         'DOUBLE'
    }
);

-- Quick sanity check after load
SELECT
    COUNT(*)              AS row_count,
    COUNT(DISTINCT region) AS region_count,
    SUM(CASE WHEN region = 'NA' THEN 1 ELSE 0 END) AS north_america_orders
FROM ecommerce_orders;
