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
            material_name = col.replace("Material_", "")
            material_name = material_name.replace("_", " ")
            return material_name

    return "Unknown Material"


def recommend_material(weight, volume, fragility):

    weight = float(weight)
    volume = float(volume)
    fragility = int(fragility)

    # Keep values in valid range
    fragility = max(1, min(5, fragility))

    data = df.copy()

    # -------------------------------------------------
    # Normalize user inputs
    # -------------------------------------------------

    # Dataset values are between 0 and 1
    weight_score = min(weight / 500.0, 1.0)
    volume_score = min(volume / 5000.0, 1.0)
    fragility_score = fragility / 5.0

    # -------------------------------------------------
    # Eco Score
    # -------------------------------------------------

    data["eco_score"] = (
        (1 - data["CO2_Emission_Score_kg"]) * 40 +
        data["Biodegradability_Score"] * 25 +
        data["Recyclability_Percentage"] * 20 +
        (1 - data["Price_INR"]) * 15
    )

    # -------------------------------------------------
    # Weight Matching
    # -------------------------------------------------

    data["weight_match"] = 1 - abs(
        data["Weight_Capacity_kg"] - weight_score
    )

    # -------------------------------------------------
    # Volume Matching
    # -------------------------------------------------

    data["volume_match"] = 1 - abs(
        data["Material_Suitability_Score"] - volume_score
    )

    # -------------------------------------------------
    # Fragility Matching
    # -------------------------------------------------

    data["fragility_match"] = (
        data["Strength_MPa"] * fragility_score
    )

    # -------------------------------------------------
    # Final Score
    # -------------------------------------------------

    data["final_score"] = (
        data["eco_score"] * 0.40 +
        data["weight_match"] * 20 +
        data["volume_match"] * 15 +
        data["fragility_match"] * 25
    )

    # -------------------------------------------------
    # Sort Results
    # -------------------------------------------------

    data_sorted = data.sort_values(
        by="final_score",
        ascending=False
    )

    best = data_sorted.iloc[0]

    # -------------------------------------------------
    # Ranking
    # -------------------------------------------------

    ranking = []

    for _, row in data_sorted.head(20).iterrows():

        ranking.append({

            "material": row["Material_ID"],

            "material_name": get_material_name(row),

            "price_inr": round(float(row["Price_INR"]), 2),

            "cost_index": round(float(row["Cost_Efficiency_Index"]), 3),

            "co2": round(float(row["CO2_Emission_Score_kg"]), 3),

            "eco_score": round(float(row["eco_score"]), 2)

        })

    # -------------------------------------------------
    # Return JSON
    # -------------------------------------------------

    return {

        "best_material": best["Material_ID"],

        "best_material_name": get_material_name(best),

        "best_price_inr": round(float(best["Price_INR"]), 2),

        "best_cost_index": round(float(best["Cost_Efficiency_Index"]), 3),

        "best_eco_score": round(float(best["eco_score"]), 2),

        "ranking": ranking

    }