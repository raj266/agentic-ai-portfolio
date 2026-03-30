import csv
import sqlite3

# Global cache for the property data (either a list or a SQLite connection)
_PROPERTIES_CACHE = None
_THRESHOLD = 500  # Use SQLite when rows exceed this number

def _load_properties():
    """Load CSV once and return either a list or an in‑memory SQLite connection."""
    global _PROPERTIES_CACHE
    if _PROPERTIES_CACHE is not None:
        return _PROPERTIES_CACHE

    # Read CSV
    with open("properties.csv", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        for row in rows:
            row["price_cr"] = float(row["price_cr"])
            row["bhk"] = int(row["bhk"])

    # Choose storage based on size
    if len(rows) < _THRESHOLD:
        # Use list
        _PROPERTIES_CACHE = rows
    else:
        # Use in‑memory SQLite
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE properties (
                name TEXT,
                price_cr REAL,
                bhk INTEGER,
                area TEXT,
                possession TEXT,
                legal_status TEXT,
                connectivity TEXT
            )
        ''')
        for row in rows:
            cursor.execute('''
                INSERT INTO properties VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (row['name'], row['price_cr'], row['bhk'],
                  row['area'], row['possession'], row['legal_status'],
                  row['connectivity']))
        # Create indexes
        cursor.execute('CREATE INDEX idx_area ON properties(area)')
        cursor.execute('CREATE INDEX idx_price ON properties(price_cr)')
        cursor.execute('CREATE INDEX idx_bhk ON properties(bhk)')
        conn.commit()
        _PROPERTIES_CACHE = conn
    return _PROPERTIES_CACHE

def _query_list(func, *args):
    """Helper to run a query on the list‑based cache."""
    data = _load_properties()
    # data is a list
    return func(data, *args)

def _query_db(func, *args):
    """Helper to run a query on the SQLite cache."""
    conn = _load_properties()
    # conn is a sqlite3.Connection
    return func(conn, *args)

# ----------------------------------------------------------------------
# Public tool functions
# ----------------------------------------------------------------------
def search_listings(budget_min, budget_max, bhk):
    cache = _load_properties()
    if isinstance(cache, list):
        # List search
        results = [p for p in cache if budget_min <= p["price_cr"] <= budget_max and p["bhk"] == bhk]
        return results
    else:
        # SQLite search
        cursor = cache.cursor()
        cursor.execute('''
            SELECT * FROM properties
            WHERE price_cr BETWEEN ? AND ? AND bhk = ?
        ''', (budget_min, budget_max, bhk))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def check_legal_status(location):
    cache = _load_properties()
    if isinstance(cache, list):
        for p in cache:
            if p["area"].lower() == location.lower():
                return p["legal_status"]
        return "Unknown"
    else:
        cursor = cache.cursor()
        cursor.execute('SELECT legal_status FROM properties WHERE area = ?', (location,))
        row = cursor.fetchone()
        return row["legal_status"] if row else "Unknown"

def check_connectivity(location):
    cache = _load_properties()
    if isinstance(cache, list):
        for p in cache:
            if p["area"].lower() == location.lower():
                return p["connectivity"]
        return "Unknown"
    else:
        cursor = cache.cursor()
        cursor.execute('SELECT connectivity FROM properties WHERE area = ?', (location,))
        row = cursor.fetchone()
        return row["connectivity"] if row else "Unknown"

def calculate_total_cost(price_cr):
    stamp = price_cr * 0.05
    reg = price_cr * 0.015
    return {
        "base": price_cr,
        "stamp": round(stamp, 2),
        "registration": round(reg, 2),
        "total": round(price_cr + stamp + reg, 2)
    }