-- =============================================================================
-- 11_high_discount_impact.sql — Low vs medium vs high discount comparison
-- =============================================================================
-- Depends on: stg_orders_profit
--
-- Discount groups (business thresholds):
--   Low discount    : discount < 15%
--   Medium discount : 15% <= discount < 25%
--   High discount   : discount >= 25%
-- =============================================================================

WITH base AS (
    SELECT
        *,
        CASE
            WHEN discount < 0.15 THEN 'Low discount (< 15%)'
            WHEN discount < 0.25 THEN 'Medium discount (15% to 25%)'
            ELSE 'High discount (>= 25%)'
        END AS discount_group
    FROM stg_orders_profit
),

group_metrics AS (
    SELECT
        discount_group,
        COUNT(*)                                                    AS orders,
        ROUND(SUM(revenue), 2)                                      AS revenue,
        ROUND(SUM(profit), 2)                                       AS profit,
        ROUND(100.0 * SUM(profit) / NULLIF(SUM(revenue), 0), 2)     AS profit_margin_pct,
        ROUND(
            100.0 * SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)
            / NULLIF(COUNT(*), 0),
            2
        )                                                           AS loss_making_order_rate_pct
    FROM base
    GROUP BY discount_group
)

SELECT
    discount_group,
    orders,
    revenue,
    profit,
    profit_margin_pct,
    loss_making_order_rate_pct
FROM group_metrics
ORDER BY
    CASE discount_group
        WHEN 'Low discount (< 15%)'           THEN 1
        WHEN 'Medium discount (15% to 25%)'   THEN 2
        WHEN 'High discount (>= 25%)'         THEN 3
        ELSE 99
    END;
