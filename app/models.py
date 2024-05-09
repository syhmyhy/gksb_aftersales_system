# app/models.py

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

class Job(db.Model):
    __tablename__ = 'job'
    jobNo = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    custName = db.Column(db.String(255), nullable=False)
    vehicleType = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    dateReceived = db.Column(db.Date, nullable=False)
    costUnit = db.Column(db.Numeric(65, 2), nullable=False)  # Assuming costUnit is a decimal field
    totalCost = db.Column(db.Numeric(65, 2), nullable=False)  # Assuming totalCost is a decimal field
    profitUnit = db.Column(db.Numeric(65, 2), nullable=False)  # Assuming profitUnit is a decimal field
    totalProfit = db.Column(db.Numeric(65, 2), nullable=False)  # Assuming totalProfit is a decimal field
    jobDateDelivered = db.Column(db.Date, nullable=False)
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    aftersales_count = db.Column(db.Integer, default=0)  # New field to track aftersales entries

    # Method to check if aftersales limit is reached
    def is_aftersales_limit_reached(self):
        return self.aftersales_count >= self.quantity
    
class Staff(db.Model):
    __tablename__ = 'staff'
    staffID = db.Column(db.Integer, primary_key=True)
    staffEmail = db.Column(db.String(255), nullable=False)  # Add email field
    firstName = db.Column(db.String(255), nullable=False)
    lastName = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(45), nullable=False)
    role = db.Column(db.String(255), nullable=False)