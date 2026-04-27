-- Assumed table name: ecommerce_orders
-- Columns:
-- order_id, customer_id, product_category, region, order_date, revenue, cost, discount

-- 1) Total profit
SELECT
    SUM(revenue - cost) AS total_profit,
    SUM(revenue) AS total_revenue,
    100.0 * SUM(revenue - cost) / NULLIF(SUM(revenue), 0) AS overall_profit_margin_pct
FROM ecommerce_orders;


-- 2) Profit per category
SELECT
    product_category,
    SUM(revenue) AS total_revenue,
    SUM(revenue - cost) AS total_profit,
    AVG(discount) AS avg_discount,
    100.0 * SUM(revenue - cost) / NULLIF(SUM(revenue), 0) AS profit_margin_pct
FROM ecommerce_orders
GROUP BY product_category
ORDER BY total_profit DESC;


-- 3) Profit per region
SELECT
    region,
    SUM(revenue) AS total_revenue,
    SUM(revenue - cost) AS total_profit,
    AVG(discount) AS avg_discount,
    100.0 * SUM(revenue - cost) / NULLIF(SUM(revenue), 0) AS profit_margin_pct
FROM ecommerce_orders
GROUP BY region
ORDER BY total_profit DESC;


-- 4) Average discount impact on profit
SELECT
    CASE
        WHEN discount < 0.05 THEN '0-5%'
        WHEN discount < 0.10 THEN '5-10%'
        WHEN discount < 0.15 THEN '10-15%'
        WHEN discount < 0.20 THEN '15-20%'
        WHEN discount < 0.25 THEN '20-25%'
        WHEN discount < 0.30 THEN '25-30%'
        ELSE '30%+'
    END AS discount_band,
    COUNT(*) AS orders,
    AVG(revenue - cost) AS avg_profit_per_order,
    SUM(revenue - cost) AS total_profit,
    100.0 * AVG((revenue - cost) / NULLIF(revenue, 0)) AS avg_profit_margin_pct
FROM ecommerce_orders
GROUP BY 1
ORDER BY
    CASE
        WHEN discount_band = '0-5%' THEN 1
        WHEN discount_band = '5-10%' THEN 2
        WHEN discount_band = '10-15%' THEN 3
        WHEN discount_band = '15-20%' THEN 4
        WHEN discount_band = '20-25%' THEN 5
        WHEN discount_band = '25-30%' THEN 6
        ELSE 7
    END;
