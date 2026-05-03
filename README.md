## Dashboard preview

![Dashboard](dashboard.png)

# E-commerce profit leak analysis

Portfolio case for **junior Data Analyst / Business Analyst** roles: connect order-level data to a clear profitability story, segment leaks, quantify discount risk, and turn findings into prioritized actions a commercial team can use.

---

## The profitability problem (what the business is really solving)

Revenue looks healthy, but **margin is thin and uneven**. In this dataset the business books **$2,054,589.16** revenue and **$214,040.75** profit, so the **overall margin is 10.42%** across **12,000** orders (January 2024 → December 2025)—i.e. **about 10.4 cents of profit per dollar of revenue** on average—acceptable only if it is stable and deliberate. The analysis shows it is not: **specific categories and regions lose money**, and **deep discounting turns volume into negative profit**. The core question is not “Are we selling?” but **“Which sales build profit, and which erode it?”**

---

## Key profit leaks (ranked by business urgency)

These are the main **structural leaks** called out in the analysis—each ties to a segment or behavior you can monitor and fix.

| Priority | Leak | What the data shows | Why it matters |
|----------|------|---------------------|----------------|
| 1 | **Electronics in EU** | Profit **-$42,103.66**, margin **-17.53%**, average discount **30.25%** | Largest single drain; this segment alone erodes **nearly 20%** of total company profit ($42,103.66 vs $214,040.75). |
| 2 | **EU region overall** | Revenue **$533,005.54** but profit only **$5,890.14**, margin **1.11%** | High revenue with almost no margin suggests pricing, discount, or cost-to-serve issues concentrated in Europe—not a “small market” problem. |
| 3 | **Home & Kitchen in LATAM** | Profit **-$3,983.51**, margin **-8.37%** | Secondary loss pocket; worth fixing after the EU/Electronics crisis or in parallel if resources allow. |
| 4 | **Loss-making orders** | **16.01%** of orders are loss-making | One in six orders destroys value at the transaction level—weak governance on price and discount unless strategically intentional. |

**Context:** Other regions in the same outputs perform much stronger on margin (for example **NA ~15.1%** and **APAC ~15.6%** profit margin on revenue in `outputs/profit_by_region.csv`), which makes the **EU at 1.11%** stand out as a **regional profitability imbalance**, not a universal slowdown.

---

## Discount impact (how promotions hurt or help)

Discounting is not “neutral” here—it **separates profitable volume from value destruction**.

- **Orders with discount ≥ 25%** generated **-$40,234.94** profit in aggregate.
- **Orders with discount below 15%** generated **$166,114.56** profit in aggregate.

So **aggressive tiers** are associated with **negative total profit**, while **lighter discounting** carries most of the **positive** profit in the file. Margin also **collapses by discount band**:

- **0–5% discount:** **34.84%** margin  
- **30–45% discount:** **-14.75%** margin  

**Business read:** the company is at risk of **buying revenue with discounts** that the P&L cannot support. Any promotion or approval workflow should be checked against **margin at band**, not only uplift in units or revenue.

---

## Priority actions (what to do first)

Actions below **only restate recommendations supported by the numbers above**—no new ROI or savings targets are invented.

1. **P0 — Stop unguarded deep discounts**  
   Introduce **margin-based discount guardrails** (caps and approvals by category/region, alerts before margin goes negative). Directly addresses the **≥25% discount** loss pool and the **Electronics / EU** discount level (**30.25%** average).

2. **P0 — EU commercial reset**  
   **EU pricing, promotions, and cost-to-serve** need a focused review: the region has **strong revenue** but **1.11%** margin. Align with the **Electronics in EU** deep dive first, then roll out region-wide controls.

3. **P1 — LATAM Home & Kitchen**  
   Investigate **costs, suppliers, logistics, and promo depth** for the **-$3,983.51 / -8.37%** segment so fixes are targeted, not guesswork.

4. **P1 — Shift from volume-only KPIs**  
   Pair revenue targets with **margin, loss-making order rate, and band-level profitability** so teams are not rewarded for sales that lose money.

---

## Dashboard usage (how a BA or lead would use this week to week)

The dashboard image (`dashboard.png`) and the **`outputs/`** artifacts are meant to support a **short weekly or monthly review**—same metrics, refreshed data:

| Stakeholder question | Where to look |
|----------------------|----------------|
| Are we improving overall profitability? | Total revenue, profit, overall margin (dataset summary / summary tiles). |
| Which region is dragging margin? | Region view — watch **EU** vs **NA/APAC** margin contrast. |
| Which category burns cash? | Category × region — **Electronics EU** and **Home & Kitchen LATAM** as named leaks. |
| Are promotions still safe? | Discount bands — **≥25%** vs **below 15%** profit totals; **0–5%** vs **30–45%** margin bands. |
| How bad is transaction-level leakage? | **16.01%** loss-making orders — trend this down over time. |

**Cadence:** Operations and finance can use the same cuts (region, category, discount band) to **catch leaks early** instead of discovering them quarterly.

---

## Expected business impact (directional, no invented savings)

The analysis does **not** estimate a dollar “uplift” from fixes (that would require pilots and forecasting). **Qualitatively**, if guardrails and EU/LATAM actions work as intended, the business should see:

- **Fewer loss-making orders** (currently **16.01%** of orders).  
- **Protected margin** on high-discount campaigns (today **≥25%** discounts sum to **negative** profit).  
- **Stabilized EU profitability** without requiring proportional revenue growth (EU today: **$533,005.54** revenue, **$5,890.14** profit).  
- **A more sustainable growth model** where promotions are tested against **margin**, not only top-line.

The largest **numerical** opportunity already in the story is **closing or repricing the Electronics EU leak (-$42,103.66)** and **reducing reliance on the discount bands that show negative margin**.

---

## Objectives

- Identify loss-making segments across product categories and regions  
- Analyze the impact of discounting on profitability  
- Detect structural weaknesses in business performance  
- Provide data-driven recommendations to restore margin  

---

## Project structure

```text
01_profit_leak_case/
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
└── requirements.txt
```

---

## Dataset overview

| Metric | Value |
|--------|--------|
| Total orders | 12,000 |
| Revenue | $2,054,589.16 |
| Profit | $214,040.75 |
| Overall margin | 10.42% |
| Date range | January 2024 → December 2025 |

**Dimensions:** product category, region, customer ID, order date, discount.

**Columns:** `order_id`, `customer_id`, `product_category`, `region`, `order_date`, `revenue`, `cost`, `discount`

---

## Analytical approach

- **Profit at order level:** profit = revenue − cost  
- **Segment performance:** category and region  
- **Discount impact:** bands and thresholds (e.g. ≥25% vs below 15%)  
- **Loss concentration:** worst segments and share of loss-making orders  

---

## Additional insights (supporting detail)

- **Electronics EU** remains the headline leak (figures in table above).  
- **Discount strategy:** high discounts are not producing profitable growth in this slice—the **≥25%** vs **below 15%** profit split makes that explicit.  
- **Secondary segment:** **Home & Kitchen LATAM** at **-$3,983.51** and **-8.37%** margin suggests cost or pricing issues beyond discounting alone.  
- **Governance:** **16.01%** loss-making orders points to weak **pricing and promotion controls** unless those orders are strategically subsidized.

---

## Strategic diagnosis (summary)

1. **Uncontrolled discounting** — deep discounts can turn revenue into losses; the band analysis supports strict controls.  
2. **Regional imbalance** — EU revenue without margin vs stronger regions in the same export set.  
3. **Limited profitability monitoring** — leadership needs visibility on **segments, discount bands, regions, and loss-making order share** to act before margin erodes.

---

## Recommendations (detailed)

1. **Margin-based discount guardrails** — category/region caps, approvals above **25%**, alerts when projected margin is negative (targets the documented discount loss).  
2. **Profit-driven growth** — favor targeted promos, loyalty, segmentation, and margin-aware campaigns instead of blanket discounts.  
3. **Fix EU pricing and cost mix** — reduce excessive discounting, review pricing, review logistics/ops cost, weekly category margin reviews.  
4. **Home & Kitchen LATAM** — validate supplier, shipping, fulfillment, and promotion exposure; renegotiate or reprice as findings support.  
5. **Profit leak monitoring dashboard** — track revenue, profit, overall margin, margin by region/category, discount-band profitability, top loss-making segments, and **percentage of loss-making orders**.

---

## How to run the project

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

Results are saved under **`outputs/`**: cleaned dataset with profit, profit by category/region, discount impact, top customers, worst segments, charts, and **`key_findings_summary.json`**.

**SQL:** `sql/profit_analysis_queries.sql` reproduces main aggregates (total profit, profit by category/region, discount bands, loss-making segments).

---

## Tools used

Python, pandas, matplotlib, SQL, CSV analysis, business analytics, data storytelling.

---

## Interview explanation (short pitch)

I analyzed e-commerce orders to explain why **strong revenue did not translate into strong profitability**. I built **profit at order level**, then cut the data by **category, region, and discount**. The standout was **Electronics in the EU** as the largest leak, with **negative margin** and **high average discount**. I also showed that **orders discounted ≥25%** summed to **negative profit**, while **lower-discount** orders carried **positive** profit. My recommendations were **margin-based discount guardrails**, a **focused EU pricing and promo review**, and a **weekly profit-leak dashboard** aligned to the same KPIs.

---

## Skills demonstrated

Data cleaning, profitability analysis, SQL, business KPI analysis, discount impact analysis, loss-making segmentation, visualization, recommendations, analytical storytelling.

---

## Conclusion

The profitability problem is **not** primarily “too little revenue.” It is **margin erosion in specific segments and discount tiers**, with **Electronics EU** first priority, **EU regional margin** second, **Home & Kitchen LATAM** third, and **deep discounting** as a cross-cutting lever. **Controlling discounts**, **monitoring margins**, and **tightening EU (and LATAM) commercial execution** can improve profit **without** assuming revenue must grow—using only the patterns and magnitudes already present in the data.
