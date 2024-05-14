# app\models\staff_model.py

from app import db

class Staff(db.Model):
    __tablename__ = 'staff'
    staffID = db.Column(db.String(10), primary_key=True)
    staffEmail = db.Column(db.String(255), nullable=False)  # Add email field
    staffName = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(45), nullable=False)
    role = db.Column(db.String(255), nullable=False)