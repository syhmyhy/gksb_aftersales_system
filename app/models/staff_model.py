# app\models\staff_model.py

from app import db

class Staff(db.Model):
    __tablename__ = 'staff'
    staffID = db.Column(db.String(10), primary_key=True)
    staffEmail = db.Column(db.String(255), nullable=False)
    staffName = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(45), nullable=False)
    role = db.Column(db.String(255), nullable=False)
    approved = db.Column(db.Boolean, default=False, nullable=False)  # Add approved field
