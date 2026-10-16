import requests
import pandas as pd

session = requests.Session()

def get_datacite(prefix):
    print(f"Contacting DataCite to retreive info for {prefix}")
    r = session.get(f"https://api.datacite.org/prefixes/{prefix}", timeout=15)
    if r.status_code == 404:
        return []
    r.raise_for_status()
    data = r.json()["data"]["relationships"]["clients"]["data"]
    return [c["id"] for c in data]

def get_crossref(prefix):
    print(f"Contacting Crossref to retreive info for {prefix}")
    r = session.get(f"https://api.crossref.org/prefixes/{prefix}", timeout=15)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()["message"].get("name")

def lookup(prefix):
    try:
        clients = get_datacite(prefix)
    except Exception as e:
        print(f"DataCite failed for {prefix}: {type(e).__name__}: {e}")
        clients = []

    if clients:
        return clients[0]

    try:
        name = get_crossref(prefix)
    except Exception as e:
        print(f"Crossref failed for {prefix}: {type(e).__name__}: {e}")
        return {"source": "error", "client": None}

    if name:
        return name
    return {"source": None, "client": []}

domain_counts = pd.read_csv("domain_counts.csv", encoding="utf-8")
prefix_counts = pd.read_csv("prefix_counts.csv", encoding="utf-8", dtype={"prefix": str})

prefixes = prefix_counts["prefix"].dropna().unique()[:30]
clients_by_prefix = {p: lookup(p) for p in prefixes}

prefix_counts["clients"] = prefix_counts["prefix"].map(clients_by_prefix)

prefix_counts.to_csv("prefix_counts_enriched.csv", encoding="utf-8", index=False)

print(domain_counts, prefix_counts)