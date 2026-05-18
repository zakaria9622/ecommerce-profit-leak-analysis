# Methodology — E-commerce Profit Leak Analysis

## Project purpose

This portfolio project is a **profit leak analysis** case study. The business question is not only whether the company sells enough, but **where revenue fails to translate into profit** — and what actions can restore margin.

The analysis focuses on:

- Revenue and profit at order level
- Margin erosion by product category, region, and segment
- Discount impact on profitability
- Unprofitable (loss-making) orders and segments
- Data-driven recommendations for commercial and pricing teams

---

## Core metrics

All metrics are derived from order-level data unless stated otherwise.

| Metric | Definition |
|--------|------------|
| **Revenue** | Order revenue (`revenue`) |
| **Cost** | Order cost (`cost`) |
| **Profit** | `profit = revenue - cost` |
| **Profit margin** | `profit_margin = profit / revenue` (expressed as % in reporting) |
| **Discount** | Discount rate applied to the order (`discount`, e.g. `0.25` = 25%) |

Aggregations (sums, averages, counts) are built on these base fields by dimension.

---

## Core analysis dimensions

| Dimension | Description |
|-----------|-------------|
| **Product category** | Product line (e.g. Electronics, Fashion, Home & Kitchen) |
| **Region** | Geographic market (NA, EU, APAC, LATAM) |
| **Category × region segment** | Combined segment; used to pinpoint profit leaks (e.g. Electronics in EU) |
| **Discount band** | Binned discount levels (e.g. 0–5%, 5–10%, …, 30–45%) |
| **Customer** | Customer-level profitability (top contributors, concentration) |
| **Month** | Time trend from `order_date` (revenue, profit, margin over time) |

---

## Tool roles in this project

| Tool | Role |
|------|------|
| **SQL** | **Source of business metrics** — aggregations, KPIs, segments, and trends run in a queryable database layer. SQL outputs define the numbers used in recommendations. |
| **Python** | **Validation and automation** — data generation, enrichment, parity checks against SQL, and scripted exports. Python confirms that pipelines and formulas are consistent. |
| **Tableau** | **Dashboard storytelling** — executive and operational views for stakeholders: KPIs, profit leaks, discount impact, and trends. Tableau presents the SQL-backed story visually. |

Workflow intent:

1. Load canonical data (`data/ecommerce_orders.csv`) into SQL (or use validated exports).
2. Run SQL for official business metrics.
3. Use Python to validate, automate, and optionally regenerate supporting files.
4. Build Tableau dashboards on canonical data or SQL/Python outputs — not on deprecated cleaned files unless the NA region issue is resolved.

---

## Analytical approach (high level)

1. Calculate profit and margin at order level.
2. Aggregate by category, region, discount band, customer, and month.
3. Identify loss-making segments (category × region, discount tiers).
4. Quantify discount impact on margin.
5. Translate findings into prioritized business recommendations.

See also:

- [data_dictionary.md](data_dictionary.md) — column and field definitions
- [business_questions.md](business_questions.md) — questions this project answers
