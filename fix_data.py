import pandas as pd

# Load dataset
df = pd.read_csv("data/ecommerce_orders.csv")

# Fix missing regions
df["region"] = df["region"].fillna("Unknown")

# Recalculate profit
df["profit"] = df["revenue"] - df["cost"]

# Convert discount to percentage (optional display)
df["discount_pct"] = df["discount"] * 100

# Clean columns (rename for readability)
df = df.rename(columns={
    "order_id": "Order ID",
    "customer_id": "Customer ID",
    "product_category": "Category",
    "order_date": "Order Date",
    "revenue": "Revenue",
    "cost": "Cost",
    "discount": "Discount",
    "region": "Region",
    "profit": "Profit"
})

# Save clean dataset
df.to_csv("data/cleaned_dataset.csv", index=False)

print("✅ Clean dataset created: data/cleaned_dataset.csv")