import os

class Config:
    SECRET_KEY = "mysecretkey"
    DATABASE_URL=os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
