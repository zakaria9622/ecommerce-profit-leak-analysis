# SQL layer — E-commerce profit leak analysis

DuckDB-compatible SQL scripts for profitability analysis: revenue, cost, profit, margin, discounts, loss-making orders, category × region segments, and monthly trends.

---

## Canonical data source

| Use | File |
|-----|------|
| **Yes** | `data/ecommerce_orders.csv` |
| **No** | `data/cleaned_dataset.csv` |

Do **not** use `data/cleaned_dataset.csv` for SQL or Tableau. A legacy cleaning step may treat region code **NA** (North America) as missing and replace it with **Unknown**, which breaks regional KPIs.

See also: [../docs/data_dictionary.md](../docs/data_dictionary.md)

---

## How to run (DuckDB)

From the **repository root**:

```bash
# Create database and load canonical CSV
duckdb data/profit_leak.duckdb < sql/01_load_duckdb.sql

# Create staging view
duckdb data/profit_leak.duckdb < sql/02_staging_profit_view.sql

# Run any analysis query (examples)
duckdb data/profit_leak.duckdb < sql/03_kpi_overview.sql
duckdb data/profit_leak.duckdb < sql/06_category_region_segments.sql
```

Interactive session:

```bash
duckdb data/profit_leak.duckdb
```

```sql
.read sql/01_load_duckdb.sql
.read sql/02_staging_profit_view.sql
.read sql/03_kpi_overview.sql
```

> `data/profit_leak.duckdb` is ignored by `.gitignore` (local database file).

Optional: run `sql/00_schema.sql` first if you prefer an empty table before load; `01_load_duckdb.sql` recreates the table from CSV.

---

## Run order

| Step | File | Purpose |
|------|------|---------|
| 0 | `00_schema.sql` | Optional — DDL for `ecommerce_orders` |
| 1 | `01_load_duckdb.sql` | Load `data/ecommerce_orders.csv` |
| 2 | `02_staging_profit_view.sql` | Create view `stg_orders_profit` |
| 3–11 | `03_kpi_overview.sql` … `11_high_discount_impact.sql` | Business metrics (any order after step 2) |

Legacy file (unchanged): `profit_analysis_queries.sql` — early reference queries; prefer `03`–`11` for the full analysis.

---

## File guide

| File | Output focus |
|------|----------------|
| `03_kpi_overview.sql` | Executive KPIs (revenue, profit, margin, loss-making rate) |
| `04_profit_by_category.sql` | Profit by product category |
| `05_profit_by_region.sql` | Profit by region |
| `06_category_region_segments.sql` | Category × region profit leaks + rank |
| `07_discount_impact.sql` | Margin by discount band |
| `08_top_customers.sql` | Top 10 customers by profit |
| `09_loss_making_orders.sql` | Loss-making order summary |
| `10_monthly_trend.sql` | Monthly trend for dashboards |
| `11_high_discount_impact.sql` | Low / medium / high discount comparison |

All analysis queries read from **`stg_orders_profit`** (profit, margin, discount bands, `order_month`).

---

## Tool roles in this project

| Tool | Role |
|------|------|
| **SQL** | **Source of business metrics** — official aggregates for recommendations and reporting |
| **Python** | Validation and automation (`scripts/analyze_profit_leaks.py`, dataset generation) |
| **Tableau** | Dashboard storytelling (planned — will connect to canonical data or SQL/Python outputs) |

---

## Key definitions

```text
profit          = revenue - cost
profit_margin   = profit / revenue
discount_band   = 0-5%, 5-10%, …, 30-45% (aligned with Python)
loss-making     = profit < 0 at order level
```

Region **NA** = North America (not NULL).
