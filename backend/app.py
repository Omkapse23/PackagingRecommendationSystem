from flask import Flask
from flask_cors import CORS
from routes.recommendation_routes import recommendation_bp
from routes.dashboard_routes import dashboard_bp
import os

app = Flask(__name__)
CORS(app)

app.register_blueprint(recommendation_bp)
app.register_blueprint(dashboard_bp)

@app.route("/")
def home():
    return {"status": "Backend is running"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
