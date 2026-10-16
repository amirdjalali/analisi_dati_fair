import pandas as pd

m = pd.read_csv("map.csv", encoding="utf-8", na_values=["None"])
prefix_counts = pd.read_csv("prefix_counts_enriched.csv", encoding="utf-8", dtype={"prefix": str})
domain_counts = pd.read_csv("domain_counts.csv", encoding="utf-8")

dom_map = m.dropna(subset=["domain"]).drop_duplicates("domain").set_index("domain")["normalized"]
cli_map = m.dropna(subset=["clients"]).drop_duplicates("clients").set_index("clients")["normalized"]

def normalize(df, key, mapping):
    out = df.copy()
    in_map = out[key].isin(mapping.index)
    out["name"] = out[key].map(mapping)
    # key is in the map but normalized is None -> remove
    out = out[~(in_map & out["name"].isna())].copy()
    # key not in the map at all -> keep its original value as the name
    out["name"] = out["name"].fillna(out[key])
    return out[["name", "count"]]

combined = (
    pd.concat(
        [normalize(domain_counts, "domain", dom_map),
         normalize(prefix_counts, "clients", cli_map)],
        ignore_index=True,
    )
    .groupby("name", as_index=False)["count"].sum()
    .sort_values("count", ascending=False)
    .reset_index(drop=True)
)

combined.to_csv("combined_counts.csv", index=False)

