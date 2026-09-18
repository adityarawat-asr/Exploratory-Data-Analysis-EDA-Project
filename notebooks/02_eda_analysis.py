"""
Exploratory Data Analysis (EDA) on the E-Commerce Customer Behavior dataset.
Produces statistical summaries (printed + saved) and visualizations (saved as PNG).
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="viridis")
plt.rcParams["figure.dpi"] = 150

DATA_PATH = "/home/claude/eda_project/data/ecommerce_customer_data.csv"
IMG_DIR = "/home/claude/eda_project/images"

df = pd.read_csv(DATA_PATH)

# ---------------------------------------------------------------
# 1. Basic info & statistical summary
# ---------------------------------------------------------------
print("Shape:", df.shape)
print(df.info())

summary = df.describe(include="all").transpose()
summary.to_csv("/home/claude/eda_project/data/summary_statistics.csv")
print(summary)

# ---------------------------------------------------------------
# 2. Correlation heatmap (numeric features)
# ---------------------------------------------------------------
numeric_cols = ["Age", "AnnualIncome_USD", "SpendingScore", "NumPurchasesPerYear",
                 "PurchaseAmount_USD", "TenureMonths", "SatisfactionScore", "Churned"]
corr = df[numeric_cols].corr()

plt.figure(figsize=(9, 7))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdYlGn", center=0,
            linewidths=0.5, square=True, cbar_kws={"shrink": 0.8})
plt.title("Correlation Heatmap of Numeric Features", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{IMG_DIR}/01_correlation_heatmap.png")
plt.close()

# ---------------------------------------------------------------
# 3. Distribution of key numeric variables
# ---------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
sns.histplot(df["Age"], bins=25, kde=True, ax=axes[0, 0], color="#4C72B0")
axes[0, 0].set_title("Age Distribution")

sns.histplot(df["AnnualIncome_USD"], bins=25, kde=True, ax=axes[0, 1], color="#55A868")
axes[0, 1].set_title("Annual Income Distribution")

sns.histplot(df["PurchaseAmount_USD"], bins=25, kde=True, ax=axes[1, 0], color="#C44E52")
axes[1, 0].set_title("Purchase Amount Distribution")

sns.histplot(df["SatisfactionScore"], bins=20, kde=True, ax=axes[1, 1], color="#8172B2")
axes[1, 1].set_title("Satisfaction Score Distribution")

plt.tight_layout()
plt.savefig(f"{IMG_DIR}/02_distributions.png")
plt.close()

# ---------------------------------------------------------------
# 4. Purchase Amount vs Spending Score (scatter, colored by category)
# ---------------------------------------------------------------
plt.figure(figsize=(9, 6))
sns.scatterplot(data=df, x="SpendingScore", y="PurchaseAmount_USD",
                 hue="ProductCategory", alpha=0.7, s=45)
plt.title("Purchase Amount vs Spending Score by Product Category", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{IMG_DIR}/03_spending_vs_purchase.png")
plt.close()

# ---------------------------------------------------------------
# 5. Average purchase amount by region & category (bar)
# ---------------------------------------------------------------
plt.figure(figsize=(10, 6))
region_cat = df.groupby("Region")["PurchaseAmount_USD"].mean().sort_values(ascending=False)
sns.barplot(x=region_cat.index, y=region_cat.values, palette="crest")
plt.title("Average Purchase Amount by Region", fontsize=13, fontweight="bold")
plt.ylabel("Avg Purchase Amount (USD)")
plt.tight_layout()
plt.savefig(f"{IMG_DIR}/04_avg_purchase_by_region.png")
plt.close()

# ---------------------------------------------------------------
# 6. Churn rate by satisfaction bucket
# ---------------------------------------------------------------
df["SatisfactionBucket"] = pd.cut(df["SatisfactionScore"], bins=[0, 2, 3, 4, 5],
                                   labels=["1-2 (Low)", "2-3", "3-4", "4-5 (High)"])
churn_rate = df.groupby("SatisfactionBucket", observed=True)["Churned"].mean() * 100

plt.figure(figsize=(8, 5.5))
sns.barplot(x=churn_rate.index, y=churn_rate.values, palette="rocket")
plt.title("Churn Rate (%) by Satisfaction Bucket", fontsize=13, fontweight="bold")
plt.ylabel("Churn Rate (%)")
plt.xlabel("Satisfaction Score Bucket")
plt.tight_layout()
plt.savefig(f"{IMG_DIR}/05_churn_by_satisfaction.png")
plt.close()

# ---------------------------------------------------------------
# 7. Product category popularity
# ---------------------------------------------------------------
plt.figure(figsize=(8, 5.5))
cat_counts = df["ProductCategory"].value_counts()
sns.barplot(x=cat_counts.values, y=cat_counts.index, palette="mako")
plt.title("Number of Customers by Product Category", fontsize=13, fontweight="bold")
plt.xlabel("Count")
plt.tight_layout()
plt.savefig(f"{IMG_DIR}/06_category_popularity.png")
plt.close()

# ---------------------------------------------------------------
# 8. Boxplot: Income by Region
# ---------------------------------------------------------------
plt.figure(figsize=(9, 6))
sns.boxplot(data=df, x="Region", y="AnnualIncome_USD", palette="Set2")
plt.title("Annual Income Distribution by Region", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{IMG_DIR}/07_income_by_region_box.png")
plt.close()

print("\nAll charts saved to:", IMG_DIR)

# ---------------------------------------------------------------
# Key insight numbers used in the README
# ---------------------------------------------------------------
insights = {
    "corr_income_purchase": round(corr.loc["AnnualIncome_USD", "PurchaseAmount_USD"], 2),
    "corr_spending_purchase": round(corr.loc["SpendingScore", "PurchaseAmount_USD"], 2),
    "corr_satisfaction_churn": round(corr.loc["SatisfactionScore", "Churned"], 2),
    "top_region": region_cat.idxmax(),
    "top_region_avg": round(region_cat.max(), 2),
    "top_category": cat_counts.idxmax(),
    "top_category_count": int(cat_counts.max()),
    "overall_churn_rate": round(df["Churned"].mean() * 100, 1),
    "low_satisfaction_churn": round(churn_rate.iloc[0], 1),
    "high_satisfaction_churn": round(churn_rate.iloc[-1], 1),
    "avg_purchase": round(df["PurchaseAmount_USD"].mean(), 2),
    "median_income": round(df["AnnualIncome_USD"].median(), 2),
}
print("\nKEY INSIGHTS:")
for k, v in insights.items():
    print(f"  {k}: {v}")

pd.Series(insights).to_csv("/home/claude/eda_project/data/key_insights.csv")
