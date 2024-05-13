# app\aftersales_model.py

from app import db

class Aftersales(db.Model):
    __tablename__ = 'aftersales'
    jobNo = db.Column(db.Integer, db.ForeignKey('job.jobNo'))
    endUser = db.Column(db.String(255), nullable=False)
    bodyType = db.Column(db.String(255), nullable=False)
    chassisType = db.Column(db.String(255), nullable=False)
    chassisModel = db.Column(db.String(255), nullable=False)
    chassisNo = db.Column(db.String(255), nullable=False)
    engineNo = db.Column(db.String(255), nullable=False)
    registrationNo = db.Column(db.String(10), nullable=False, primary_key=True)
    dateDelivered = db.Column(db.DATETIME, nullable=False)
    stateLocality = db.Column(db.String(45), nullable=False)
    detailLocality = db.Column(db.String(255), nullable=False)
    chassisMileageWarranty = db.Column(db.Integer, nullable=False)
    chassisPeriodWarranty = db.Column(db.Integer, nullable=False)
    chassisExpired = db.Column(db.DateTime, nullable=False)
    bodyPeriodWarranty = db.Column(db.Integer, nullable=False)
    bodyExpired = db.Column(db.DateTime, nullable=False)
    noService = db.Column(db.Integer, nullable=False)
    mileageService = db.Column(db.Integer, nullable=False)
    custPhone = db.Column(db.String(20))
    custEmail = db.Column(db.String(255))
    notes = db.Column(db.String(255))