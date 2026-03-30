import csv

_PROPERTIES_CACHE = None

def load_properties():
    global _PROPERTIES_CACHE
    if _PROPERTIES_CACHE is None:
        with open("properties.csv", newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            for row in rows:
                row["price_cr"] = float(row["price_cr"])
                row["bhk"] = int(row["bhk"])
            _PROPERTIES_CACHE = rows
    return _PROPERTIES_CACHE

def search_listings(budget_min, budget_max, bhk):
    all_props = load_properties()
    return [p for p in all_props if budget_min <= p["price_cr"] <= budget_max and p["bhk"] == bhk]

def check_legal_status(location):
    all_props = load_properties()
    for p in all_props:
        if p["area"].lower() == location.lower():
            return p["legal_status"]
    return "Unknown"

def check_connectivity(location):
    all_props = load_properties()
    for p in all_props:
        if p["area"].lower() == location.lower():
            return p["connectivity"]
    return "Unknown"

def calculate_total_cost(price_cr):
    stamp = price_cr * 0.05
    reg = price_cr * 0.015
    return {
        "base": price_cr,
        "stamp": round(stamp, 2),
        "registration": round(reg, 2),
        "total": round(price_cr + stamp + reg, 2)
    }
