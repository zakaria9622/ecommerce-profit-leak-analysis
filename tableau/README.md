# Tableau — Profit leak dashboard (planned)

This folder will hold the **Tableau workbook** for the e-commerce profit leak analysis. The workbook is not included yet; it will be added in a later phase.

---

## Data source rules

The dashboard must be built from:

- **Canonical data:** `data/ecommerce_orders.csv`, or
- **Validated outputs** from the SQL or Python pipeline (e.g. enriched order table, aggregate exports)

**Do not use** `data/cleaned_dataset.csv` unless the **NA region issue** is fixed. That file may map the region code **NA** (North America) to **Unknown**, which breaks regional analysis.

See [../docs/data_dictionary.md](../docs/data_dictionary.md) for column definitions and calculated fields.

---

## Expected dashboard sections

| Section | Purpose |
|---------|---------|
| **Executive KPI cards** | Total revenue, total profit, overall margin, key leak indicators |
| **Profit by category** | Compare profitability across product categories |
| **Profit by region** | Compare profitability across regions |
| **Category × region profit leak view** | Highlight worst segments (profit leaks) |
| **Discount impact on margin** | Margin and profit by discount band |
| **Monthly profit trend** | Revenue and profit over time by month |
| **Top customers** | Most profitable customers by aggregated profit |

These sections align with [../docs/business_questions.md](../docs/business_questions.md).

---

## Future workbook location

When the dashboard is built, save the workbook here as:

- `tableau/profit_leak_dashboard.twb`, or
- `tableau/profit_leak_dashboard.twbx` (packaged workbook with data, if needed)

A static preview image may continue to live at the repository root as `dashboard.png` for GitHub README display.

---

## Tool context

- **SQL** — source of business metrics  
- **Python** — validation and automation  
- **Tableau** — stakeholder-facing dashboard storytelling  

See [../docs/methodology.md](../docs/methodology.md).
