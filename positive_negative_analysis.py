import pandas as pd


df = pd.read_csv("all_articles - FINAL DATASET.csv")


category_col = "positive/neutral/negative"
sentiment_col = "open coding/categories"


df[sentiment_col] = df[sentiment_col].str.lower().str.strip()


summary = (
    df.groupby([category_col, sentiment_col])
      .size()
      .reset_index(name="count")
)


total_per_cat = (
    df.groupby(category_col)
      .size()
      .reset_index(name="total")
)


summary = summary.merge(total_per_cat, on=category_col)


summary["percent"] = (summary["count"] / summary["total"] * 100).round(2)


summary.to_csv("sentiment_percentages_by_category.csv", index=False)

print("\nSaved:")
print(" • sentiment_percentages_by_category.csv")
