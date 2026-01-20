# 📦 EcoPackAI – AI-Powered Sustainable Packaging Recommendation System  

EcoPackAI is an AI-powered packaging recommendation system that suggests the **best eco-friendly packaging material** based on product characteristics like **weight**, **volume**, and **fragility**.  
It uses machine learning models + an eco-score ranking logic to generate a **ranked list of packaging materials**, helping users choose sustainable packaging.

---

## 🏢 Internship Details  
**Project Type:** Infosys Springboard Virtual Internship (AI Domain)  
**Duration:** 6 Weeks (Milestone 1–3)  
**Completion Date:** January 2026  
**Technology Stack:** Python, MySQL, Flask, Machine Learning, HTML, CSS, JavaScript  

---

## ✨ Key Features  
- ✅ Eco-friendly packaging recommendation system  
- ✅ Dataset preprocessing + feature engineering  
- ✅ ML models for prediction  
  - Random Forest (Cost Prediction)
  - XGBoost (CO₂ Prediction)
- ✅ AI-based ranking using eco-score + cost index  
- ✅ Flask backend API (`/predict`)  
- ✅ Frontend UI with dynamic results + ranking table  

---

## 🏗️ Project Architecture  

```
┌──────────────────────────────────────────────────────────┐
│                 Web Interface (Frontend)                 │
│              HTML + CSS + JavaScript                     │
│     (Input Form + Best Recommendation + Ranking Table)   │
└──────────────────────────┬───────────────────────────────┘
                           │ HTTP/JSON  POST /predict
┌──────────────────────────▼───────────────────────────────┐
│                 Flask Backend API                         │
│   Flask + CORS + Blueprint Routes + JSON Responses        │
│   app.py → recommendation_routes.py → ai_model.py         │
└───────────────┬───────────────────────────┬──────────────┘
                │                           │
┌───────────────▼───────────────┐   ┌──────▼──────────────┐
│     AI / ML Recommendation     │   │      MySQL DB        │
│  eco_score + cost index rank   │   │  eco_packaging DB    │
│  Reads cleaned_materials.csv   │   │  product table model │
└───────────────────────────────┘   └──────────────────────┘
```

---

## 📌 Milestone Summary  

### ✅ Milestone 1 – Data Collection & Preprocessing  
**Completed Tasks**
- Imported dataset and stored inside **MySQL database**
- Connected MySQL with Jupyter Notebook using `mysql.connector`
- Performed Data Quality Checks:
  - Dataset shape
  - Missing values
  - Duplicates
  - `df.describe()`
- Outlier Detection (IQR Method)
- Outlier Treatment (Clipping)
- Exported cleaned dataset

**Output Files**
- `data.csv`
- `cleaned_materials.csv`

---

### ✅ Milestone 2 – Feature Engineering & Machine Learning  
**Completed Tasks**
- Feature engineering + encoding
- Created engineered dataset with extra features
- Prepared ML pipeline (train-test split + scaling)
- Trained models and evaluated performance

📌 **Actual Evaluation Results**
- **Random Forest (Cost Prediction)**
  - RMSE: `0.03425175`
  - MAE: `0.01396171`
  - R² Score: `0.98610537`

- **XGBoost (CO₂ Prediction)**
  - RMSE: `0.00118505`
  - MAE: `0.00099652`
  - R² Score: `0.99998250`

---

### ✅ Milestone 3 – Backend + Frontend Integration  
**Completed Tasks**
- Flask backend API with CORS + Blueprint routing
- Main endpoints:
  - `GET /` (health check)
  - `POST /predict` (recommendation + ranking)
- Web frontend UI:
  - input form (weight, volume, fragility)
  - best material display
  - ranking table display

---

## 🔌 API Endpoints  

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Backend status check |
| POST | `/predict` | Returns best recommendation + ranking |

---

## 🧪 Example API Request  

```json
POST /predict
{
  "weight": 2.5,
  "volume": 800,
  "fragility": 4
}
```

## ✅ Example API Response  

```json
{
  "best_material": 101,
  "best_price_inr": 750.5,
  "best_cost_index": 0.652,
  "best_eco_score": 98.4,
  "ranking": [
    {
      "material": 101,
      "price_inr": 750.5,
      "cost_index": 0.652,
      "co2": 1.6,
      "eco_score": 98.4
    }
  ]
}
```

---

## 📂 Project Structure  

```
Packaging-Recommendation-System/
│ README.md
│ requirements.txt
│ Project_Documentation.md
│
├── notebooks/
│   module1.ipynb
│   module2.ipynb
│   module3.ipynb
│   module4.ipynb
│
├── dataset/
│   data.csv
│   cleaned_materials.csv
│
├── backend/
│   app.py
│   config.py
│   database.py
│   models.py
│   recommendation_routes.py
│   product_routes.py
│   ai_model.py
│   env_score.py
│
└── frontend/
    index.html
    style.css
    app.js
```

---

## ⚙️ Installation & Setup  

### 1️⃣ Clone Repository  
```bash
git clone <your-repository-url>
cd Packaging-Recommendation-System
```

### 2️⃣ Install Dependencies  
```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Project  

### ✅ Run Backend  
```bash
python app.py
```

Backend will start at:
```
http://127.0.0.1:5000
```

### ✅ Run Frontend  
Open `frontend/index.html` using:
- VS Code Live Server (recommended)

---

## 🚀 Future Enhancements  
- Add more endpoints (`/predict/cost`, `/predict/co2`, `/materials`)
- Store recommendation history in MySQL
- Improve ranking using weighted composite scoring
- Cloud deployment (Render / Railway / AWS)