-- =============================================================================
-- 08_top_customers.sql — Top 10 customers by total profit
-- =============================================================================
-- Depends on: stg_orders_profit
-- =============================================================================

WITH base AS (
    SELECT *
    FROM stg_orders_profit
),

customer_metrics AS (
    SELECT
        customer_id,
        COUNT(*)                                                    AS orders,
        ROUND(SUM(revenue), 2)                                      AS revenue,
        ROUND(SUM(profit), 2)                                       AS profit,
        ROUND(100.0 * SUM(profit) / NULLIF(SUM(revenue), 0), 2)     AS profit_margin_pct,
        ROUND(100.0 * AVG(discount), 2)                             AS average_discount_pct
    FROM base
    GROUP BY customer_id
),

ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (ORDER BY profit DESC) AS customer_profit_rank
    FROM customer_metrics
)

SELECT
    customer_id,
    orders,
    revenue,
    profit,
    profit_margin_pct,
    average_discount_pct,
    customer_profit_rank
FROM ranked
WHERE customer_profit_rank <= 10
ORDER BY customer_profit_rank;
