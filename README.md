# E-commerce Profit Leak Analysis — Margin, Discount & Regional Profitability

![Dashboard preview](dashboard.png)

Portfolio case for **junior Data Analyst / Business Analyst** roles.

This project connects order-level data to a clear profitability story: where the company makes money, where it loses margin, how discounting affects profit, and which actions a business team should prioritize.

---

## Executive summary

Revenue looks healthy, but margin is thin and uneven.

In this dataset, the business generated:

- **$2,054,589.16** revenue
- **$214,040.75** profit
- **10.42%** overall profit margin
- **12,000** orders
- Period analyzed: **January 2024 → December 2025**

The analysis shows that the profitability issue is not caused by low revenue. The problem is **margin erosion in specific regions, product categories and discount bands**.

Main findings:

- **Electronics in EU** is the largest profit leak: **-$42,103.66** profit and **-17.53%** margin.
- **EU region overall** generates **$533,005.54** revenue but only **$5,890.14** profit, with a margin of **1.11%**.
- **Orders with discount ≥ 25%** generated **-$40,234.94** profit.
- **16.01%** of orders are loss-making.

Main business conclusion: the company should not only chase revenue. It should monitor profit by region, category and discount band, and introduce margin-based discount guardrails.

---

## The profitability problem

The core question is not:

> Are we selling enough?

The real question is:

> Which sales build profit, and which sales destroy it?

A business can grow revenue while destroying margin if discounts, costs or regional execution are not controlled. This project shows how a Data Analyst can identify those leaks and turn them into business recommendations.

---

## Key profit leaks

| Priority | Leak | What the data shows | Why it matters |
|---|---|---|---|
| 1 | **Electronics in EU** | Profit **-$42,103.66**, margin **-17.53%**, average discount **30.25%** | Largest single drain. This segment alone erodes nearly 20% of total company profit. |
| 2 | **EU region overall** | Revenue **$533,005.54**, profit only **$5,890.14**, margin **1.11%** | High revenue with almost no margin suggests pricing, discount or cost-to-serve issues. |
| 3 | **Home & Kitchen in LATAM** | Profit **-$3,983.51**, margin **-8.37%** | Secondary loss pocket that needs targeted review. |
| 4 | **Loss-making orders** | **16.01%** of orders are loss-making | One in six orders destroys value at transaction level. |

Other regions perform much better on margin. This makes the EU result stand out as a regional profitability imbalance, not a general business slowdown.

---

## Discount impact

Discounting is not neutral in this dataset.

- Orders with discount **≥ 25%** generated **-$40,234.94** profit.
- Orders with discount **below 15%** generated **$166,114.56** profit.

Margin also collapses by discount band:

| Discount band | Profit margin |
|---|---:|
| 0–5% | **34.84%** |
| 30–45% | **-14.75%** |

Business interpretation:

The company is at risk of buying revenue with discounts that the profit and loss cannot support. Promotional decisions should be reviewed against margin, not only against revenue or units sold.

---

## Priority actions

### P0 — Stop unguarded deep discounts

Introduce margin-based discount guardrails:

- discount caps by category and region
- approval workflow above a certain discount threshold
- alerts when projected margin becomes negative
- weekly review of discount-band profitability

This directly addresses the negative profit from orders discounted at **25% or more**.

### P0 — EU commercial reset

EU has strong revenue but almost no margin.

Recommended review:

- pricing strategy
- promotion depth
- logistics and cost-to-serve
- category-level margin
- especially **Electronics in EU**

### P1 — LATAM Home & Kitchen investigation

Home & Kitchen in LATAM shows negative profitability. The business should review:

- supplier costs
- shipping and fulfillment
- local pricing
- promotional exposure

### P1 — Shift from volume-only KPIs

Revenue alone is not enough.

Recommended KPIs:

- revenue
- profit
- profit margin
- loss-making order rate
- discount-band margin
- category × region profitability

---

## Dashboard usage

The dashboard image and the outputs in `outputs/` are designed for weekly or monthly business review.

| Stakeholder question | Where to look |
|---|---|
| Are we improving overall profitability? | Total revenue, profit and overall margin |
| Which region is dragging margin? | Region view, especially EU vs NA/APAC |
| Which category burns cash? | Category × region analysis |
| Are promotions still safe? | Discount-band profitability |
| How bad is transaction-level leakage? | Loss-making order rate |

The goal is to catch profit leaks early instead of discovering them after quarterly results.

---

## Expected business impact

This project does not claim a tested financial uplift. That would require experiments, pilots or updated operational data.

However, if the recommended actions work, the business should expect:

- fewer loss-making orders
- better margin control on high-discount campaigns
- improved EU profitability
- more sustainable growth
- less dependence on revenue growth alone

The largest numerical opportunity shown in the data is closing or repricing the **Electronics EU** leak and reducing reliance on discount bands that generate negative margin.

---

## What I would present to a business team

Problem:

The company generates strong revenue, but profitability is weakened by specific loss-making segments and aggressive discounting.

Finding:

Electronics in EU generated **-$42,103.66** profit with a **-17.53%** margin, while orders discounted at **25% or more** generated **-$40,234.94** profit in aggregate.

Decision:

Introduce margin-based discount guardrails, review EU pricing, and monitor profitability by region, category and discount band.

Expected impact:

Reduce loss-making orders, protect margin, and improve profit quality without depending only on revenue growth.

---

## Objectives

- Identify loss-making segments across product categories and regions.
- Analyze the impact of discounting on profitability.
- Detect structural weaknesses in business performance.
- Provide data-driven recommendations to restore margin.
- Translate technical analysis into business actions.

---

## Project structure

```text
ecommerce-profit-leak-analysis/
├── data/
│   └── ecommerce_orders.csv
├── scripts/
│   ├── generate_dataset.py
│   └── analyze_profit_leaks.py
├── sql/
│   └── profit_analysis_queries.sql
├── outputs/
│   ├── ecommerce_orders_with_profit.csv
│   ├── profit_by_category.csv
│   ├── profit_by_region.csv
│   ├── discount_impact.csv
│   ├── top_10_profitable_customers.csv
│   ├── worst_loss_making_segments.csv
│   ├── profit_by_category.png
│   ├── profit_by_region.png
│   ├── discount_impact_on_margin.png
│   ├── top_10_profitable_customers.png
│   ├── worst_loss_making_segments.png
│   └── key_findings_summary.json
├── dashboard.png
├── requirements.txt
└── README.md
```

---

## Dataset overview

| Metric | Value |
|---|---:|
| Total orders | 12,000 |
| Revenue | $2,054,589.16 |
| Profit | $214,040.75 |
| Overall margin | 10.42% |
| Date range | January 2024 → December 2025 |

Dimensions:

- product category
- region
- customer ID
- order date
- discount

Columns:

```text
order_id
customer_id
product_category
region
order_date
revenue
cost
discount
```

---

## Analytical approach

The analysis follows a simple business logic:

1. Calculate profit at order level.
2. Calculate profit margin.
3. Aggregate performance by product category.
4. Aggregate performance by region.
5. Analyze discount bands.
6. Identify loss-making segments.
7. Export CSV, JSON and chart outputs.
8. Translate findings into business recommendations.

Main formulas:

```text
profit = revenue - cost
profit_margin = profit / revenue
```

---

## SQL analysis

The SQL file reproduces the main business aggregates:

- total revenue
- total profit
- overall profit margin
- profit by category
- profit by region
- discount-band profitability
- loss-making segments

SQL is included to show that the analysis can be translated into a database environment, not only Python.

---

## Tools used

- Python
- pandas
- matplotlib
- SQL
- CSV analysis
- business analytics
- data storytelling

---

## How to reproduce

Run the project from the repository root.

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate the dataset

```bash
python scripts/generate_dataset.py
```

### 3. Run the analysis

```bash
python scripts/analyze_profit_leaks.py
```

### 4. Review outputs

Main outputs are generated in:

```text
outputs/
```

Expected outputs:

```text
outputs/key_findings_summary.json
outputs/profit_by_category.csv
outputs/profit_by_region.csv
outputs/discount_impact.csv
outputs/worst_loss_making_segments.csv
outputs/top_10_profitable_customers.csv
outputs/profit_by_category.png
outputs/profit_by_region.png
outputs/discount_impact_on_margin.png
outputs/worst_loss_making_segments.png
```

---

## Dataset note

This project uses a portfolio e-commerce order dataset to demonstrate a complete business profitability analysis workflow.

The goal is to show how a Data Analyst can move from raw order-level data to profit metrics, margin diagnosis, discount analysis, visual outputs and business recommendations.

The analysis does not claim real company performance or tested business impact. Recommendations are directional and should be validated with business review, experiments or updated operational data.

---

## Interview explanation

I analyzed e-commerce orders to explain why strong revenue did not translate into strong profitability.

I built profit at order level, then cut the data by category, region and discount band. The standout issue was Electronics in EU, which showed negative profit and negative margin. I also found that orders discounted at 25% or more generated negative profit overall.

My recommendations were to introduce margin-based discount guardrails, review EU pricing and promotions, and monitor profitability weekly by region, category and discount band.

---

## Skills demonstrated

- Data cleaning
- Profitability analysis
- Business KPI analysis
- SQL aggregation
- Python analysis with pandas
- Discount impact analysis
- Loss-making segmentation
- Data visualization
- Business recommendations
- Analytical storytelling

---

## Conclusion

The profitability problem is not mainly a revenue problem.

It is a margin erosion problem concentrated in specific segments and discount tiers. Electronics in EU is the first priority, EU regional margin is the second priority, Home & Kitchen in LATAM is the third priority, and deep discounting is the cross-cutting lever.

Controlling discounts, monitoring margins and tightening commercial execution can improve profit quality without assuming revenue growth.