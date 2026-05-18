# E-commerce Profit Leak Analysis — SQL & Tableau Dashboard

![Profit Leak Dashboard](dashboard.png)

**Portfolio project for Data Analyst / BI Analyst roles (alternance).**

This project analyzes e-commerce profitability to identify where revenue does not translate into profit, using **SQL**, **Python** and **Tableau**. The workflow moves from order-level data to business metrics, profit leak segments, discount impact, and actionable recommendations.

**Period analyzed:** January 2024 → December 2025 · **12,000 orders**

---

## Stack

| Layer | Role |
|-------|------|
| **SQL / DuckDB** | Schema, staging view, KPI queries, profit leak segments, discount impact, monthly trend — **source of business metrics** |
| **Python / pandas** | Dataset generation, validation and export automation |
| **Tableau** | Profitability dashboard and business visualization |
| **CSV outputs** | Tableau-ready aggregated files in `outputs/tableau/` |

---

## Key results

| KPI | Value |
|-----|------:|
| Total orders | 12,000 |
| Total revenue | $2,054,589 |
| Total profit | $214,041 |
| Profit margin | 10.42% |
| Average discount | 17.39% |
| Loss-making order rate | 16.01% |

---

## Main business insight

The main profit leak is concentrated in the **Electronics / EU** segment, while **high discount levels** strongly reduce margin. The priority is to **control discounting**, **review pricing rules**, and **monitor weak category–region segments** before scaling revenue.

Supporting findings:

| Focus | Insight |
|-------|---------|
| Worst segment | Electronics / EU — **-$42,104** profit, **-17.53%** margin |
| Weak region | EU — high revenue, **1.11%** margin |
| Deep discounts | Orders with discount **≥ 25%** — negative aggregate profit |
| Loss-making orders | **16.01%** of orders have `profit < 0` |

---

## SQL methodology

- **Canonical data source:** `data/ecommerce_orders.csv`
- **Core formulas:**
  - `profit = revenue - cost`
  - `profit_margin = profit / revenue`
- **Analysis dimensions:** product category, region, category × region, discount band, customer, month
- **Loss-making orders:** orders where `profit < 0`
- **SQL is the source of business metrics**; Python validates and exports; Tableau presents the story

SQL layer (`sql/`):

| File | Purpose |
|------|---------|
| `00_schema.sql` | Raw table definition |
| `01_load_duckdb.sql` | Load canonical CSV into DuckDB |
| `02_staging_profit_view.sql` | View `stg_orders_profit` (profit, margin, discount bands) |
| `03`–`11` | KPIs, category, region, segments, discounts, customers, trends |

See [sql/README.md](sql/README.md) for run order and details.

---

## Tableau artifacts

| Artifact | Description |
|----------|-------------|
| [dashboard.png](dashboard.png) | Dashboard preview (GitHub) |
| [tableau/profit_leak_dashboard.twb](tableau/profit_leak_dashboard.twb) | Tableau workbook |

Expected dashboard views: executive KPIs, profit by category and region, category × region profit leaks, discount impact on margin, monthly profit trend, top customers.

---

## Tableau-ready exports (`outputs/tableau/`)

Semicolon-delimited CSV files (`;`) for French Tableau locale, generated from SQL via DuckDB:

- `outputs/tableau/kpi_overview.csv`
- `outputs/tableau/profit_by_category.csv`
- `outputs/tableau/profit_by_region.csv`
- `outputs/tableau/category_region_segments.csv`
- `outputs/tableau/discount_impact.csv`
- `outputs/tableau/top_customers.csv`
- `outputs/tableau/loss_making_orders.csv`
- `outputs/tableau/monthly_trend.csv`
- `outputs/tableau/high_discount_impact.csv`

---

## Data warning

> **Do not use** `data/cleaned_dataset.csv` as the source of truth. A previous cleaning step may transform the region value **NA** (North America) into **Unknown**, which breaks regional analysis.
>
> **Canonical source:** `data/ecommerce_orders.csv`

See [docs/data_dictionary.md](docs/data_dictionary.md).

---

## Repository structure

```text
01_profit_leak_case/
├── data/
│   └── ecommerce_orders.csv          # Canonical source
├── sql/                              # DuckDB SQL layer (00–11)
├── scripts/
│   ├── generate_dataset.py           # Synthetic data
│   ├── analyze_profit_leaks.py       # Python validation & charts
│   └── export_tableau_outputs.py       # DuckDB → outputs/tableau/
├── outputs/
│   └── tableau/                      # Tableau-ready CSV exports
├── tableau/
│   └── profit_leak_dashboard.twb
├── docs/                             # Methodology, data dictionary, business questions
├── dashboard.png
├── requirements.txt
└── README.md
```

---

## How to reproduce

From the repository root:

```bash
pip install -r requirements.txt
```

**1. Generate data (optional — CSV already included)**

```bash
python scripts/generate_dataset.py
```

**2. Export SQL metrics for Tableau**

```bash
python scripts/export_tableau_outputs.py
```

Creates `data/profit_leak.duckdb` and refreshes `outputs/tableau/*.csv`.

**3. Python validation (optional)**

```bash
python scripts/analyze_profit_leaks.py
```

Writes additional aggregates and charts under `outputs/`.

**4. Tableau**

Open `tableau/profit_leak_dashboard.twb` or connect to `outputs/tableau/` CSVs or `data/profit_leak.duckdb`.

---

## Business recommendations

| Priority | Action |
|----------|--------|
| **P0** | Margin-based discount guardrails (caps by category/region, approval above threshold) |
| **P0** | EU commercial reset — pricing, promotions, cost-to-serve; focus on Electronics / EU |
| **P1** | Monitor category × region segments weekly (profit, margin, loss-making rate) |
| **P1** | Shift KPIs from revenue-only to profit, margin, discount-band performance |

---

## Skills demonstrated

- SQL (DuckDB): CTEs, aggregations, `CASE`, window functions, staging views
- Python: pandas, pipeline automation, export to Tableau-ready files
- Tableau: KPI dashboard, profitability and discount storytelling
- Business analysis: profit leaks, margin erosion, discount impact, recommendations

---

## Documentation

- [docs/methodology.md](docs/methodology.md) — metrics, dimensions, tool roles
- [docs/data_dictionary.md](docs/data_dictionary.md) — canonical schema and calculated fields
- [docs/business_questions.md](docs/business_questions.md) — analytical questions answered
- [tableau/README.md](tableau/README.md) — dashboard and data source rules

---

## Dataset note

Synthetic portfolio dataset for demonstration. Results are directional and do not represent real company performance. Recommendations should be validated with business review and operational data.

---

## Interview pitch (60 seconds)

I analyzed e-commerce orders to find where revenue fails to convert into profit. I built a **DuckDB SQL layer** for official KPIs — profit by category, region, and segment, discount bands, and loss-making order rate — then exported **Tableau-ready files** and built a **profitability dashboard**.

The main leak is **Electronics in EU**; **high discounts** erode margin. I recommend **discount guardrails**, **EU pricing review**, and **weekly monitoring** of weak category–region segments before pushing revenue growth.
