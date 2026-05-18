# Data dictionary

## Canonical source of truth

**File:** `data/ecommerce_orders.csv`

This is the **only** input file that should be used for SQL loads, Python analysis, and future Tableau connections.

| Property | Value |
|----------|--------|
| Grain | One row per order |
| Format | CSV, comma-separated |
| Date format | ISO (`YYYY-MM-DD`) recommended in source file |

---

## Input columns (`data/ecommerce_orders.csv`)

| Column | Type | Description |
|--------|------|-------------|
| `order_id` | string | Unique order identifier (e.g. `O100001`) |
| `customer_id` | string | Customer identifier (e.g. `C10001`) |
| `product_category` | string | Product category (e.g. Electronics, Fashion, Home & Kitchen, Beauty, Sports, Toys) |
| `region` | string | Sales region: **NA**, **EU**, **APAC**, **LATAM** |
| `order_date` | date | Order date |
| `revenue` | numeric | Order revenue after discount (currency units) |
| `cost` | numeric | Order cost (currency units) |
| `discount` | numeric | Discount rate as a decimal (e.g. `0.15` = 15%) |

---

## Calculated fields

These fields are **not** in the raw CSV; they are computed in SQL, Python, or Tableau.

| Field | Formula / logic | Notes |
|-------|-----------------|--------|
| `profit` | `revenue - cost` | Can be negative (loss-making order) |
| `profit_margin` | `profit / revenue` | Ratio; multiply by 100 for % in reports. Guard against `revenue = 0`. |
| `discount_band` | Bucket `discount` into bands | Example bands used in analysis: 0–5%, 5–10%, 10–15%, 15–20%, 20–25%, 25–30%, 30–45% |
| `month` | Derived from `order_date` | e.g. `YYYY-MM` or first day of month for monthly trends |

---

## Region code: NA

**NA** means **North America**, not a missing value.

When loading CSVs in tools that treat `NA` as null (pandas default, some ETL tools), use explicit options (e.g. `keep_default_na=False` in pandas) so North American orders are not misclassified.

---

## Warning — do not use `data/cleaned_dataset.csv` as source of truth

**File:** `data/cleaned_dataset.csv` (legacy / alternate export)

> **Important:** Do **not** use `data/cleaned_dataset.csv` as the canonical source for SQL, Tableau, or new analysis.

A previous cleaning step may treat the region value **`NA` as missing** and replace it with **`Unknown`**, which corrupts North America segmentation and any region-level KPIs.

| Use this | Do not use for new work |
|----------|-------------------------|
| `data/ecommerce_orders.csv` | `data/cleaned_dataset.csv` (until NA handling is fixed and documented) |

For methodology and tool roles, see [methodology.md](methodology.md).
