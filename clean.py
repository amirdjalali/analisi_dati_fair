import pandas as pd
import numpy as np
import re

df_list = []

for year in range(2023,2026):
    df_list.append(pd.read_csv(f"{year}.csv", encoding="ISO-8859-1"))

df = pd.concat(df_list).dropna().rename(columns={"ï»¿dati FAIR: DOI": "doi", "dati FAIR: URL": "url"})

# treat placeholders and empty strings as missing
df[["doi", "url"]] = df[["doi", "url"]].replace(["-", ""], pd.NA)

# blank the url where a doi exists
df.loc[df["doi"].notna(), "url"] = pd.NA

print(df)

urls = (
    df["url"].str.split("; ")
    .explode()
    .str.strip()
    .drop_duplicates()
    .reset_index(drop=True)
)

doi_pattern = r"^(?:https?://)?(?:www\.|dx\.)?doi\.org/"

doi_from_urls = urls.str.extract(
    rf"{doi_pattern}(10\..+)$",
    flags=re.IGNORECASE,
    expand=False,
).dropna()

urls = urls[~urls.str.contains(doi_pattern, case=False, regex=True)].reset_index(drop=True)

urls_df = pd.DataFrame({
    "url": urls,
    "domain": urls.str.replace(r"^https?://", "", regex=True).str.split("/").str[0],
}).dropna()

dois = (
    df["doi"].str.split("; ")
    .explode()
    .str.strip()
    .drop_duplicates()
    .reset_index(drop=True)
)

dois_df = (
    pd.concat([dois, doi_from_urls], ignore_index=True)
    .str.strip()
    .drop_duplicates()
    .to_frame(name="doi")
)

dois_df["prefix"] = dois_df["doi"].str.extract(r"^(10\.\d{4,9})/", expand=False)

urls_df = pd.DataFrame({
    "url": urls,
    "domain": urls.str.replace(r"^https?://", "", regex=True).str.split("/").str[0]
}).dropna()

dois_df.to_csv("dois_df.csv", encoding="utf-8", index=False)
urls_df.to_csv("urls_df.csv", encoding="utf-8", index=False)

# urls["domain"] = (
#     urls.str.replace(r"^https?://", "", regex=True)
#         .str.split("/").str[0]
#         .loc[lambda s: s != "doi.org"]
# )

domain_counts = (
    urls_df["domain"].value_counts()
           .rename_axis("domain")
           .reset_index(name="count")
)

prefix_counts = (
    dois_df["prefix"].value_counts()
           .rename_axis("prefix")
           .reset_index(name="count")
)

print(domain_counts, prefix_counts)

domain_counts.to_csv("domain_counts.csv", encoding="utf-8", index=False)
prefix_counts.to_csv("prefix_counts.csv", encoding="utf-8", index=False)