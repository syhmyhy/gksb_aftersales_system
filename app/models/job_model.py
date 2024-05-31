# app\models\job_model.py

from app import db

class Job(db.Model):
    __tablename__ = 'job'
    jobNo = db.Column(db.String(20), primary_key=True)  # Changed to String
    title = db.Column(db.String(255), nullable=False)
    custName = db.Column(db.String(255), nullable=False)
    vehicleType = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Numeric(65, 2), nullable=False)
    dateReceived = db.Column(db.Date, nullable=False)
    salesUnit = db.Column(db.Numeric(65, 2), nullable=False)
    totalSales = db.Column(db.Numeric(65, 2), nullable=False)
    profitUnit = db.Column(db.Numeric(65, 2), nullable=False)
    totalProfit = db.Column(db.Numeric(65, 2), nullable=False)
    marginProfit = db.Column(db.FLOAT)
    jobDateDelivered = db.Column(db.Date, nullable=False)
    staffID = db.Column(db.String(10), db.ForeignKey('staff.staffID'))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    aftersales_count = db.Column(db.Integer, default=0)

    # Method to check if aftersales limit is reached
    def is_aftersales_limit_reached(self):
        return self.aftersales_count >= self.quantity