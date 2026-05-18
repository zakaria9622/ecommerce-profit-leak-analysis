-- =============================================================================
-- 03_kpi_overview.sql — Executive KPI overview
-- =============================================================================
-- Depends on: stg_orders_profit (02_staging_profit_view.sql)
-- =============================================================================

WITH base AS (
    SELECT *
    FROM stg_orders_profit
)

SELECT
    COUNT(*)                                                    AS total_orders,
    ROUND(SUM(revenue), 2)                                      AS total_revenue,
    ROUND(SUM(cost), 2)                                         AS total_cost,
    ROUND(SUM(profit), 2)                                       AS total_profit,
    ROUND(100.0 * SUM(profit) / NULLIF(SUM(revenue), 0), 2)     AS overall_profit_margin_pct,
    ROUND(100.0 * AVG(discount), 2)                             AS average_discount_pct,
    SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)                 AS loss_making_orders,
    ROUND(
        100.0 * SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0),
        2
    )                                                           AS loss_making_order_rate_pct
FROM base;
