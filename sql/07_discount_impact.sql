-- =============================================================================
-- 07_discount_impact.sql — Margin and profit by discount band
-- =============================================================================
-- Depends on: stg_orders_profit
-- Discount bands match Python pd.cut logic in analyze_profit_leaks.py
-- =============================================================================

WITH base AS (
    SELECT *
    FROM stg_orders_profit
),

band_metrics AS (
    SELECT
        discount_band,
        COUNT(*)                                                    AS orders,
        ROUND(SUM(revenue), 2)                                      AS revenue,
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
    GROUP BY discount_band
)

SELECT
    discount_band,
    orders,
    revenue,
    profit,
    profit_margin_pct,
    average_discount_pct,
    loss_making_orders,
    loss_making_order_rate_pct
FROM band_metrics
ORDER BY
    CASE discount_band
        WHEN '0-5%'    THEN 1
        WHEN '5-10%'   THEN 2
        WHEN '10-15%'  THEN 3
        WHEN '15-20%'  THEN 4
        WHEN '20-25%'  THEN 5
        WHEN '25-30%'  THEN 6
        WHEN '30-45%'  THEN 7
        ELSE 99
    END;
