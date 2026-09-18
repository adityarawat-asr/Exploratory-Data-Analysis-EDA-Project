"""
Generates a synthetic but realistic 'E-Commerce Customer Behavior' dataset
for the Exploratory Data Analysis (EDA) Project.
"""
import numpy as np
import pandas as pd

np.random.seed(42)
N = 1000

regions = ["North", "South", "East", "West", "Central"]
region_weights = [0.22, 0.20, 0.18, 0.22, 0.18]

categories = ["Electronics", "Fashion", "Home & Living", "Beauty", "Groceries", "Sports"]

genders = np.random.choice(["Male", "Female", "Other"], size=N, p=[0.47, 0.49, 0.04])
age = np.clip(np.random.normal(35, 12, N), 18, 70).round().astype(int)

# Income correlated loosely with age (career growth), with noise
annual_income = np.clip(
    18000 + age * 850 + np.random.normal(0, 9000, N), 15000, 160000
).round(-2)

# Spending score influenced by income (diminishing returns) + randomness
spending_score = np.clip(
    20 + (annual_income / 1600) - (age * 0.35) + np.random.normal(0, 12, N),
    1, 100
).round(1)

region = np.random.choice(regions, size=N, p=region_weights)
product_category = np.random.choice(categories, size=N)

# Purchase amount driven by spending score + income + category effect + noise
category_multiplier = {
    "Electronics": 1.6, "Fashion": 1.1, "Home & Living": 1.2,
    "Beauty": 0.8, "Groceries": 0.5, "Sports": 1.0
}
cat_mult = np.array([category_multiplier[c] for c in product_category])

purchase_amount = np.clip(
    (spending_score * 4.2 + annual_income * 0.004) * cat_mult
    + np.random.normal(0, 60, N),
    10, None
).round(2)

# Number of purchases per year, loosely tied to spending score
num_purchases = np.clip(
    (spending_score / 6 + np.random.normal(0, 3, N)), 1, 40
).round().astype(int)

# Membership tenure in months
tenure_months = np.random.randint(1, 73, N)

# Satisfaction score (1-5), weakly linked to tenure and purchase amount
satisfaction = np.clip(
    3 + (tenure_months / 72) + (purchase_amount / 2000) + np.random.normal(0, 0.8, N),
    1, 5
).round(1)

# Churn flag: more likely with low satisfaction & low tenure
churn_prob = np.clip(0.55 - (satisfaction / 8) - (tenure_months / 300), 0.02, 0.9)
churned = (np.random.rand(N) < churn_prob).astype(int)

df = pd.DataFrame({
    "CustomerID": [f"CUST{i:05d}" for i in range(1, N + 1)],
    "Age": age,
    "Gender": genders,
    "Region": region,
    "AnnualIncome_USD": annual_income.astype(int),
    "SpendingScore": spending_score,
    "ProductCategory": product_category,
    "NumPurchasesPerYear": num_purchases,
    "PurchaseAmount_USD": purchase_amount,
    "TenureMonths": tenure_months,
    "SatisfactionScore": satisfaction,
    "Churned": churned,
})

out_path = "/home/claude/eda_project/data/ecommerce_customer_data.csv"
df.to_csv(out_path, index=False)
print(f"Saved {len(df)} rows to {out_path}")
print(df.head())
