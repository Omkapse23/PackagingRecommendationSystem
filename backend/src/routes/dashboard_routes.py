from flask import Blueprint, request, jsonify, send_file
import pandas as pd
import os

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_PATH = os.path.join(BASE_DIR, "databases", "recommendation_history.csv")


def load_history():
    if not os.path.exists(HISTORY_PATH):
        return pd.DataFrame()

    df = pd.read_csv(HISTORY_PATH)

    # convert numeric safely
    for col in ["weight", "volume", "fragility", "best_price_inr", "best_cost_index", "best_eco_score"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


#  SUMMARY API
@dashboard_bp.route("/summary", methods=["GET"])
def summary():
    fragility = request.args.get("fragility", "all")

    df = load_history()
    if df.empty:
        return jsonify({"total": 0, "avg_eco": 0, "avg_cost": 0, "top_material": "-"}), 200

    if fragility != "all":
        df = df[df["fragility"] == int(fragility)]

    if df.empty:
        return jsonify({"total": 0, "avg_eco": 0, "avg_cost": 0, "top_material": "-"}), 200

    avg_eco = float(df["best_eco_score"].mean()) if "best_eco_score" in df.columns else 0
    avg_cost = float(df["best_cost_index"].mean()) if "best_cost_index" in df.columns else 0

    top_material = "-"
    if "best_material" in df.columns and not df["best_material"].dropna().empty:
        top_material = df["best_material"].mode()[0]

    return jsonify({
        "total": int(len(df)),
        "avg_eco": round(avg_eco, 2),
        "avg_cost": round(avg_cost, 3),
        "top_material": top_material
    })


#  TOP MATERIALS API
@dashboard_bp.route("/top-materials", methods=["GET"])
def top_materials():
    fragility = request.args.get("fragility", "all")

    df = load_history()
    if df.empty or "best_material" not in df.columns:
        return jsonify([]), 200

    if fragility != "all":
        df = df[df["fragility"] == int(fragility)]

    if df.empty:
        return jsonify([]), 200

    top = df["best_material"].value_counts().head(7)
    result = [{"material": k, "count": int(v)} for k, v in top.items()]
    return jsonify(result)


#  HISTORY JSON API (THIS WAS MISSING)
@dashboard_bp.route("/history", methods=["GET"])
def history():
    df = load_history()
    if df.empty:
        return jsonify([]), 200
    return jsonify(df.to_dict(orient="records"))


# EXPORT EXCEL API (THIS WAS MISSING)
@dashboard_bp.route("/export/excel", methods=["GET"])
def export_excel():
    df = load_history()

    export_path = os.path.join(BASE_DIR, "databases", "dashboard_report.xlsx")

    # if no history, still generate empty excel
    df.to_excel(export_path, index=False)

    return send_file(export_path, as_attachment=True)
