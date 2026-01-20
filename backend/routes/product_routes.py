from flask import Blueprint, request, jsonify
from models import Product
from database import db
from utils.ai_model import recommend_material
from utils.env_score import calculate_env_score

product_bp = Blueprint("product_bp", __name__)

@product_bp.route("/add-product", methods=["POST"])
def add_product():
    data = request.json

    material = recommend_material(
        data["weight"],
        data["fragility"]
    )

    score = calculate_env_score(material)

    product = Product(
        product_name=data["product_name"],
        weight=data["weight"],
        fragility=data["fragility"],
        material=material,
        env_score=score
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "status": "success",
        "recommended_material": material,
        "environment_score": score
    })
