import numpy as np
import pandas as pd


def build_segment_profiles(categories, regions):
    """Return realistic baseline discount and cost profiles per segment."""
    category_discount = {
        "Electronics": 0.16,
        "Fashion": 0.21,
        "Home & Kitchen": 0.13,
        "Beauty": 0.11,
        "Sports": 0.14,
        "Toys": 0.12,
    }
    category_cost_ratio = {
        "Electronics": 0.78,
        "Fashion": 0.63,
        "Home & Kitchen": 0.71,
        "Beauty": 0.58,
        "Sports": 0.67,
        "Toys": 0.62,
    }
    region_discount_shift = {
        "NA": 0.00,
        "EU": 0.03,
        "APAC": 0.01,
        "LATAM": 0.02,
    }
    region_cost_shift = {
        "NA": 0.00,
        "EU": 0.01,
        "APAC": -0.01,
        "LATAM": 0.03,
    }

    profiles = {}
    for cat in categories:
        for reg in regions:
            disc = category_discount[cat] + region_discount_shift[reg]
            cost = category_cost_ratio[cat] + region_cost_shift[reg]
            profiles[(cat, reg)] = {"discount_mean": disc, "cost_ratio_mean": cost}

    # Inject explicit "profit leak" segments.
    profiles[("Electronics", "EU")] = {"discount_mean": 0.30, "cost_ratio_mean": 0.82}
    profiles[("Home & Kitchen", "LATAM")] = {
        "discount_mean": 0.21,
        "cost_ratio_mean": 0.86,
    }
    profiles[("Fashion", "EU")] = {"discount_mean": 0.29, "cost_ratio_mean": 0.70}
    return profiles


def generate_orders(n_orders=12000, seed=42):
    rng = np.random.default_rng(seed)

    categories = ["Electronics", "Fashion", "Home & Kitchen", "Beauty", "Sports", "Toys"]
    regions = ["NA", "EU", "APAC", "LATAM"]

    segment_profiles = build_segment_profiles(categories, regions)

    category_weights = np.array([0.24, 0.19, 0.18, 0.13, 0.14, 0.12])
    region_weights = np.array([0.37, 0.28, 0.22, 0.13])

    order_ids = [f"O{100000 + i}" for i in range(n_orders)]
    customer_ids = [f"C{10000 + i}" for i in rng.integers(0, 2200, size=n_orders)]

    order_dates = pd.to_datetime(
        rng.integers(
            pd.Timestamp("2024-01-01").value // 10**9,
            pd.Timestamp("2025-12-31").value // 10**9,
            size=n_orders,
        ),
        unit="s",
    ).normalize()

    selected_categories = rng.choice(categories, size=n_orders, p=category_weights)
    selected_regions = rng.choice(regions, size=n_orders, p=region_weights)

    # Category-level ticket size distributions.
    base_price_mu = {
        "Electronics": 430,
        "Fashion": 125,
        "Home & Kitchen": 210,
        "Beauty": 85,
        "Sports": 165,
        "Toys": 105,
    }
    base_price_sigma = {
        "Electronics": 135,
        "Fashion": 55,
        "Home & Kitchen": 95,
        "Beauty": 30,
        "Sports": 70,
        "Toys": 35,
    }

    gross_values = []
    discounts = []
    costs = []

    for cat, reg in zip(selected_categories, selected_regions):
        profile = segment_profiles[(cat, reg)]

        gross = max(25.0, rng.normal(base_price_mu[cat], base_price_sigma[cat]))
        discount = np.clip(rng.normal(profile["discount_mean"], 0.05), 0.00, 0.45)
        cost_ratio = np.clip(rng.normal(profile["cost_ratio_mean"], 0.03), 0.52, 0.95)

        revenue = gross * (1 - discount)
        cost = gross * cost_ratio + rng.normal(0, 6)
        cost = max(8.0, cost)

        gross_values.append(revenue)
        discounts.append(discount)
        costs.append(cost)

    df = pd.DataFrame(
        {
            "order_id": order_ids,
            "customer_id": customer_ids,
            "product_category": selected_categories,
            "region": selected_regions,
            "order_date": order_dates,
            "revenue": np.round(gross_values, 2),
            "cost": np.round(costs, 2),
            "discount": np.round(discounts, 4),
        }
    )

    return df.sort_values("order_date").reset_index(drop=True)


if __name__ == "__main__":
    output_path = "data/ecommerce_orders.csv"
    orders = generate_orders()
    orders.to_csv(output_path, index=False)
    print(f"Dataset generated: {output_path}")
    print(f"Rows: {len(orders)}")
