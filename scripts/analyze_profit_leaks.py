import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


sns.set_theme(style="whitegrid")


def ensure_dirs():
    Path("outputs").mkdir(parents=True, exist_ok=True)


def analyze():
    ensure_dirs()
    df = pd.read_csv(
        "data/ecommerce_orders.csv",
        parse_dates=["order_date"],
        keep_default_na=False,  # keep region code "NA" as a literal label, not missing.
    )
    df["profit"] = df["revenue"] - df["cost"]
    df["profit_margin"] = df["profit"] / df["revenue"]

    # 1) Profit by product category
    by_category = (
        df.groupby("product_category", as_index=False)
        .agg(
            total_revenue=("revenue", "sum"),
            total_profit=("profit", "sum"),
            avg_discount=("discount", "mean"),
        )
        .sort_values("total_profit", ascending=False)
    )
    by_category["profit_margin_pct"] = 100 * by_category["total_profit"] / by_category["total_revenue"]

    # 2) Profit by region
    by_region = (
        df.groupby("region", as_index=False)
        .agg(
            total_revenue=("revenue", "sum"),
            total_profit=("profit", "sum"),
            avg_discount=("discount", "mean"),
        )
        .sort_values("total_profit", ascending=False)
    )
    by_region["profit_margin_pct"] = 100 * by_region["total_profit"] / by_region["total_revenue"]

    # 3) Discount impact
    discount_bins = [-0.001, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.45]
    discount_labels = [
        "0-5%",
        "5-10%",
        "10-15%",
        "15-20%",
        "20-25%",
        "25-30%",
        "30-45%",
    ]
    df["discount_band"] = pd.cut(df["discount"], bins=discount_bins, labels=discount_labels)

    discount_impact = (
        df.groupby("discount_band", observed=False, as_index=False)
        .agg(
            orders=("order_id", "count"),
            avg_profit=("profit", "mean"),
            total_profit=("profit", "sum"),
            avg_margin_pct=("profit_margin", lambda x: 100 * x.mean()),
        )
        .sort_values("discount_band")
    )

    # 4) Top 10 most profitable customers
    top_customers = (
        df.groupby("customer_id", as_index=False)
        .agg(
            total_revenue=("revenue", "sum"),
            total_profit=("profit", "sum"),
            orders=("order_id", "count"),
        )
        .sort_values("total_profit", ascending=False)
        .head(10)
    )

    # 5) Worst loss-making segments (category x region)
    worst_segments = (
        df.groupby(["product_category", "region"], as_index=False)
        .agg(
            orders=("order_id", "count"),
            total_revenue=("revenue", "sum"),
            total_profit=("profit", "sum"),
            avg_discount=("discount", "mean"),
        )
        .sort_values("total_profit", ascending=True)
        .head(10)
    )
    worst_segments["profit_margin_pct"] = 100 * worst_segments["total_profit"] / worst_segments["total_revenue"]

    # Persist tabular outputs
    by_category.to_csv("outputs/profit_by_category.csv", index=False)
    by_region.to_csv("outputs/profit_by_region.csv", index=False)
    discount_impact.to_csv("outputs/discount_impact.csv", index=False)
    top_customers.to_csv("outputs/top_10_profitable_customers.csv", index=False)
    worst_segments.to_csv("outputs/worst_loss_making_segments.csv", index=False)

    # Save enriched dataset
    df.to_csv("outputs/ecommerce_orders_with_profit.csv", index=False)

    # Visual 1: profit by category
    plt.figure(figsize=(10, 5))
    chart1 = sns.barplot(
        data=by_category,
        x="product_category",
        y="total_profit",
        hue="product_category",
        palette="viridis",
        legend=False,
    )
    chart1.set_title("Total Profit by Product Category")
    chart1.set_xlabel("Product Category")
    chart1.set_ylabel("Total Profit")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig("outputs/profit_by_category.png", dpi=150)
    plt.close()

    # Visual 2: profit by region
    plt.figure(figsize=(8, 5))
    chart2 = sns.barplot(
        data=by_region,
        x="region",
        y="total_profit",
        hue="region",
        palette="magma",
        legend=False,
    )
    chart2.set_title("Total Profit by Region")
    chart2.set_xlabel("Region")
    chart2.set_ylabel("Total Profit")
    plt.tight_layout()
    plt.savefig("outputs/profit_by_region.png", dpi=150)
    plt.close()

    # Visual 3: discount impact on margin
    plt.figure(figsize=(10, 5))
    chart3 = sns.barplot(
        data=discount_impact,
        x="discount_band",
        y="avg_margin_pct",
        hue="discount_band",
        palette="rocket",
        legend=False,
    )
    chart3.set_title("Average Profit Margin by Discount Band")
    chart3.set_xlabel("Discount Band")
    chart3.set_ylabel("Average Profit Margin (%)")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig("outputs/discount_impact_on_margin.png", dpi=150)
    plt.close()

    # Visual 4: top customers
    plt.figure(figsize=(11, 5))
    chart4 = sns.barplot(
        data=top_customers,
        x="customer_id",
        y="total_profit",
        hue="customer_id",
        palette="Blues_d",
        legend=False,
    )
    chart4.set_title("Top 10 Most Profitable Customers")
    chart4.set_xlabel("Customer ID")
    chart4.set_ylabel("Total Profit")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig("outputs/top_10_profitable_customers.png", dpi=150)
    plt.close()

    # Visual 5: worst segments
    worst_segments["segment"] = worst_segments["product_category"] + " | " + worst_segments["region"]
    plt.figure(figsize=(11, 6))
    chart5 = sns.barplot(
        data=worst_segments,
        x="segment",
        y="total_profit",
        hue="segment",
        palette="Reds_r",
        legend=False,
    )
    chart5.set_title("Worst Loss-Making Segments (Category x Region)")
    chart5.set_xlabel("Segment")
    chart5.set_ylabel("Total Profit")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig("outputs/worst_loss_making_segments.png", dpi=150)
    plt.close()

    # Create concise numeric summary for README
    total_revenue = df["revenue"].sum()
    total_profit = df["profit"].sum()
    total_margin_pct = 100 * total_profit / total_revenue
    worst_segment = worst_segments.iloc[0].to_dict()
    high_discount = df[df["discount"] >= 0.25]
    low_discount = df[df["discount"] < 0.15]

    summary = {
        "total_orders": int(df.shape[0]),
        "total_revenue": round(float(total_revenue), 2),
        "total_profit": round(float(total_profit), 2),
        "overall_margin_pct": round(float(total_margin_pct), 2),
        "worst_segment": {
            "product_category": worst_segment["product_category"],
            "region": worst_segment["region"],
            "total_profit": round(float(worst_segment["total_profit"]), 2),
            "profit_margin_pct": round(float(worst_segment["profit_margin_pct"]), 2),
            "avg_discount": round(float(worst_segment["avg_discount"]), 4),
        },
        "avg_margin_high_discount_pct": round(float(100 * high_discount["profit_margin"].mean()), 2),
        "avg_margin_low_discount_pct": round(float(100 * low_discount["profit_margin"].mean()), 2),
        "profit_gap_high_vs_low_discount_pct_points": round(
            float(100 * low_discount["profit_margin"].mean() - 100 * high_discount["profit_margin"].mean()), 2
        ),
    }

    with open("outputs/key_findings_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("Analysis complete. Check outputs/ for tables, visuals, and summary JSON.")


if __name__ == "__main__":
    analyze()
