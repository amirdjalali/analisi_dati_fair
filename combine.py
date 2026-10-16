import pandas as pd

domain_counts = pd.read_csv("domain_counts.csv", encoding="utf-8")
prefix_counts = pd.read_csv("prefix_counts.csv", encoding="utf-8")

a = domain_counts[["domain", "count"]].set_axis(["name", "count"], axis=1).assign(kind="domain")
b = prefix_counts[["clients", "count"]].set_axis(["name", "count"], axis=1).assign(kind="client")

combined = pd.concat([a, b], ignore_index=True)
combined = combined.sort_values("count", ascending=False, ignore_index=True)

combined.to_csv("combined.csv", index=False, encoding="utf-8")