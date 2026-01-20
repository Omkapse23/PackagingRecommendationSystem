from database import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100))
    weight = db.Column(db.Float)
    fragility = db.Column(db.String(50))
    material = db.Column(db.String(50))
    env_score = db.Column(db.Float)
