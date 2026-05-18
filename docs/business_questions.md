# Business questions

This project answers profitability questions for an e-commerce business using order-level data. Each question maps to SQL metrics, optional Python validation, and future Tableau views.

---

## Category profitability

**Which product categories generate the most and least profit?**

- Compare total profit, revenue, and profit margin by `product_category`.
- Highlight categories with high revenue but low or negative margin.

---

## Regional profitability

**Which regions are the least profitable?**

- Compare profit and margin across `region` (NA, EU, APAC, LATAM).
- Identify regions with strong revenue but weak margin.

---

## Segment profit leaks

**Which category × region segments create profit leaks?**

- Analyze combined `product_category` and `region`.
- Rank segments by total profit (ascending) to surface worst performers.
- Prioritize segments with negative profit or negative margin.

---

## Discount impact

**How do discounts affect margin?**

- Group orders by `discount_band`.
- Compare average and total profit, and profit margin, across bands.
- Assess whether deep discounts correlate with negative margin or loss-making orders.

---

## Loss-making orders

**What share of orders are loss-making?**

- Define loss-making as `profit < 0` at order level.
- Report count and percentage of loss-making orders.
- Use as a KPI for promotional and pricing guardrails.

---

## Customer profitability

**Which customers are the most profitable?**

- Aggregate profit and revenue by `customer_id`.
- Identify top contributors and concentration of profit among customers.

---

## Profit over time

**How does profit evolve over time?**

- Aggregate revenue, profit, and margin by `month` (from `order_date`).
- Show trends and seasonality for executive and operational review.

---

## Related documentation

- [methodology.md](methodology.md) — metrics, dimensions, and tool roles
- [data_dictionary.md](data_dictionary.md) — canonical file and field definitions
