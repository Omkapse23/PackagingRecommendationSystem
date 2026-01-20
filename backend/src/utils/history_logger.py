# backend/utils/history_logger.py

import os
import csv
from datetime import datetime

# absolute path (no path confusion)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # backend/
DB_DIR = os.path.join(BASE_DIR, "databases")
HISTORY_PATH = os.path.join(DB_DIR, "recommendation_history.csv")

# Fixed columns for dashboard (always same order)
FIELDS = [
    "timestamp",
    "weight",
    "volume",
    "fragility",
    "best_material",
    "best_price_inr",
    "best_cost_index",
    "best_eco_score",
]

def log_recommendation(inputs: dict, result: dict):
    """
    Logs prediction history to databases/recommendation_history.csv
    Always writes clean CSV with same columns (prevents pandas ParserError).
    """

    # Ensure databases folder exists
    os.makedirs(DB_DIR, exist_ok=True)

    # Prepare row
    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "weight": inputs.get("weight", ""),
        "volume": inputs.get("volume", ""),
        "fragility": inputs.get("fragility", ""),

        "best_material": result.get("best_material", ""),
        "best_price_inr": result.get("best_price_inr", ""),
        "best_cost_index": result.get("best_cost_index", ""),
        "best_eco_score": result.get("best_eco_score", ""),
    }

    # Write header only once
    file_exists = os.path.exists(HISTORY_PATH) and os.path.getsize(HISTORY_PATH) > 0

    with open(HISTORY_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)
