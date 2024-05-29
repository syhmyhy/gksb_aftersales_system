# app\models\job_model.py

from app import db

class Job(db.Model):
    __tablename__ = 'job'
    jobNo = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    custName = db.Column(db.String(255), nullable=False)
    vehicleType = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Numeric(65, 2), nullable=False)
    dateReceived = db.Column(db.Date, nullable=False)
    salesUnit = db.Column(db.Numeric(65, 2), nullable=False)  # Assuming costUnit is a decimal field
    totalSales = db.Column(db.Numeric(65, 2), nullable=False)  # Assuming totalCost is a decimal field
    profitUnit = db.Column(db.Numeric(65, 2), nullable=False)  # Assuming profitUnit is a decimal field
    totalProfit = db.Column(db.Numeric(65, 2), nullable=False)  # Assuming totalProfit is a decimal field
    marginProfit = db.Column(db.FLOAT)  # New column for marginProfit
    jobDateDelivered = db.Column(db.Date, nullable=False)
    staffID = db.Column(db.String(10), db.ForeignKey('staff.staffID'))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    aftersales_count = db.Column(db.Integer, default=0)  # New field to track aftersales entries

    # Method to check if aftersales limit is reached
    def is_aftersales_limit_reached(self):
        return self.aftersales_count >= self.quantity