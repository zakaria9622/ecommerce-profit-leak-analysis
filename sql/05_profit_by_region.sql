-- =============================================================================
-- 05_profit_by_region.sql — Profitability by region
-- =============================================================================
-- Depends on: stg_orders_profit
-- Ordered by profit ascending so weak regions appear first.
-- Region NA = North America (not a missing value).
-- =============================================================================

WITH base AS (
    SELECT *
    FROM stg_orders_profit
),

region_metrics AS (
    SELECT
        region,
        COUNT(*)                                                    AS orders,
        ROUND(SUM(revenue), 2)                                      AS revenue,
        ROUND(SUM(cost), 2)                                         AS cost,
        ROUND(SUM(profit), 2)                                       AS profit,
        ROUND(100.0 * SUM(profit) / NULLIF(SUM(revenue), 0), 2)     AS profit_margin_pct,
        ROUND(100.0 * AVG(discount), 2)                             AS average_discount_pct,
        SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)                 AS loss_making_orders,
        ROUND(
            100.0 * SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)
            / NULLIF(COUNT(*), 0),
            2
        )                                                           AS loss_making_order_rate_pct
    FROM base
    GROUP BY region
)

SELECT *
FROM region_metrics
ORDER BY profit ASC;
