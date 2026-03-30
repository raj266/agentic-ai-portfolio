import csv

def load_properties():
    properties = []
    with open("properties.csv", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["price_cr"] = float(row["price_cr"])
            row["bhk"] = int(row["bhk"])
            properties.append(row)
    return properties

def search_listings(budget_min, budget_max, bhk):
    all_props = load_properties()
    results = [p for p in all_props if budget_min <= p["price_cr"] <= budget_max and p["bhk"] == bhk]
    return results

def calculate_total_cost(price_cr):
    stamp = price_cr * 0.05
    reg = price_cr * 0.015
    return {
        "base": price_cr,
        "stamp": round(stamp, 2),
        "registration": round(reg, 2),
        "total": round(price_cr + stamp + reg, 2)
    }

def check_connectivity(location):
    all_props = load_properties()
    for p in all_props:
        if p["area"].lower() == location.lower():
            return p["connectivity"]
    return "Unknown"

def check_legal_status(location):
    all_props = load_properties()
    for p in all_props:
        if p["area"].lower() == location.lower():
            return p["legal_status"]
    return "Unknown"