-- =============================================================================
-- 10_monthly_trend.sql — Monthly profit trend (for Tableau time series)
-- =============================================================================
-- Depends on: stg_orders_profit
-- =============================================================================

WITH base AS (
    SELECT *
    FROM stg_orders_profit
),

monthly_metrics AS (
    SELECT
        order_month,
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
    GROUP BY order_month
)

SELECT *
FROM monthly_metrics
ORDER BY order_month;
