-- =============================================================================
-- 09_loss_making_orders.sql — Loss-making order summary
-- =============================================================================
-- Depends on: stg_orders_profit
-- total_loss_amount: sum of profit on loss-making orders (negative value)
-- =============================================================================

WITH base AS (
    SELECT *
    FROM stg_orders_profit
),

classified AS (
    SELECT
        *,
        profit < 0 AS is_loss_making
    FROM base
)

SELECT
    COUNT(*)                                                        AS total_orders,
    SUM(CASE WHEN is_loss_making THEN 1 ELSE 0 END)                 AS loss_making_orders,
    SUM(CASE WHEN NOT is_loss_making THEN 1 ELSE 0 END)             AS profitable_orders,
    ROUND(
        100.0 * SUM(CASE WHEN is_loss_making THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0),
        2
    )                                                               AS loss_making_order_rate_pct,
    ROUND(SUM(CASE WHEN is_loss_making THEN revenue ELSE 0 END), 2) AS revenue_from_loss_making_orders,
    ROUND(SUM(CASE WHEN is_loss_making THEN profit ELSE 0 END), 2)  AS total_loss_amount
FROM classified;
