-- =============================================================================
-- 06_category_region_segments.sql — Category × region profit leak segments
-- =============================================================================
-- Depends on: stg_orders_profit
-- Identifies worst profit leak segments (lowest profit first).
-- segment_rank_by_profit: 1 = worst segment
-- =============================================================================

WITH base AS (
    SELECT *
    FROM stg_orders_profit
),

segment_metrics AS (
    SELECT
        product_category,
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
    GROUP BY product_category, region
),

ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (ORDER BY profit ASC) AS segment_rank_by_profit
    FROM segment_metrics
)

SELECT
    product_category,
    region,
    orders,
    revenue,
    cost,
    profit,
    profit_margin_pct,
    average_discount_pct,
    loss_making_orders,
    loss_making_order_rate_pct,
    segment_rank_by_profit
FROM ranked
ORDER BY profit ASC;
