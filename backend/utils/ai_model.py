import pandas as pd
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

DATASET_PATH = os.path.join(BASE_DIR, "dataset", "cleaned_materials.csv")
df = pd.read_csv(DATASET_PATH)


def get_material_name(row):
    material_cols = [c for c in df.columns if c.startswith("Material_")]

    for col in material_cols:
        val = row.get(col)
        if str(val).upper() == "TRUE":
            return col.replace("_", " ")

    return "Unknown Material Type"


def recommend_material(weight, volume, fragility):
    weight = float(weight)
    volume = float(volume)
    fragility = int(fragility)

    if fragility < 1:
        fragility = 1
    if fragility > 5:
        fragility = 5

    data = df.copy()

    # ---------------- FILTERING (IMPORTANT) ----------------
    # Filter by weight capacity if column exists
    if "Weight_Capacity" in data.columns:
        data = data[data["Weight_Capacity"] >= (weight * 0.9)]

    # Fragility based strength filtering
    if fragility >= 4:
        if "Strength_Index" in data.columns:
            data = data[data["Strength_Index"] >= data["Strength_Index"].quantile(0.60)]
        if "Recyclability" in data.columns:
            data = data[data["Recyclability"] >= 0.4]

    # fallback if filtered dataset becomes empty
    if len(data) == 0:
        data = df.copy()

    # ---------------- ECO SCORE ----------------
    # Use CO2_Emission if available
    if "CO2_Emission" in data.columns:
        co2_min = data["CO2_Emission"].min()
        co2_max = data["CO2_Emission"].max()

        if co2_max != co2_min:
            data["co2_norm"] = (data["CO2_Emission"] - co2_min) / (co2_max - co2_min)
        else:
            data["co2_norm"] = 0

        data["eco_score"] = 100 - (data["co2_norm"] * 100)
    else:
        # fallback
        data["eco_score"] = 50

    # reward biodegradability if present
    biodeg_col = None
    for c in data.columns:
        if "Biodegrad" in c:
            biodeg_col = c
            break

    if biodeg_col:
        data["eco_score"] = data["eco_score"] + (data[biodeg_col] * 10)

    # cap eco score
    data["eco_score"] = data["eco_score"].clip(0, 100)

    # ---------------- PRICE NORMALIZATION ----------------
    # Price_INR should be real INR column
    if "Price_INR" in data.columns:
        pmin = data["Price_INR"].min()
        pmax = data["Price_INR"].max()

        if pmax != pmin:
            data["price_norm"] = (data["Price_INR"] - pmin) / (pmax - pmin)
        else:
            data["price_norm"] = 0
    else:
        data["Price_INR"] = 0
        data["price_norm"] = 0

    # ---------------- FINAL SCORE ----------------
    eco_weight = 0.6 + (fragility * 0.08)
    eco_weight = min(eco_weight, 0.95)
    price_weight = 1 - eco_weight

    data["final_score"] = (eco_weight * data["eco_score"]) - (price_weight * data["price_norm"] * 100)

    data_sorted = data.sort_values(by="final_score", ascending=False)
    best = data_sorted.iloc[0]

    # SAFE numeric fetch (prevents 0 and undefined issues)
    best_price = best.get("Price_INR", 0)
    if pd.isna(best_price):
        best_price = 0

    best_cost_index = best.get("Cost_Efficiency_Index", 0)
    if pd.isna(best_cost_index):
        best_cost_index = 0

    ranking = []
    for _, row in data_sorted.head(50).iterrows():
        price = row.get("Price_INR", 0)
        if pd.isna(price):
            price = 0

        cost_index = row.get("Cost_Efficiency_Index", 0)
        if pd.isna(cost_index):
            cost_index = 0

        ranking.append({
            "material": row["Material_ID"],
            "material_name": get_material_name(row),
            "price_inr": round(float(price), 2),
            "cost_index": round(float(cost_index), 3),
            "co2": round(float(row.get("CO2_Emission", 0) or 0), 3),
            "eco_score": round(float(row.get("eco_score", 0) or 0), 2)
        })

    return {
        "best_material": best["Material_ID"],
        "best_material_name": get_material_name(best),
        "best_price_inr": round(float(best_price), 2),
        "best_cost_index": round(float(best_cost_index), 3),
        "best_eco_score": round(float(best.get("eco_score", 0)), 2),
        "ranking": ranking
    }
