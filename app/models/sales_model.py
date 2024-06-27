# app\models\sales_model.py

from app import db

class Sales(db.Model):
    __tablename__ = 'sales'
    salesID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    salesPerson = db.Column(db.String(255), nullable=False)
    purchaseMethod = db.Column(db.String(255), nullable=False)
    tenderTitle = db.Column(db.String(255), nullable=False)
    custName = db.Column(db.String(255), nullable=True)
    chassisType = db.Column(db.String(255), nullable=True)
    chassisModel = db.Column(db.String(255), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    tenderDate = db.Column(db.Date, nullable=False)
    unitPrice = db.Column(db.Numeric(65, 2), nullable=False)
    tenderTotalPrice = db.Column(db.Numeric(65, 2), nullable=False)
    unitProfit = db.Column(db.Numeric(65, 2), nullable=False)
    tenderTotalProfit = db.Column(db.Numeric(65, 2), nullable=False)
    marginProfit = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text, nullable=True) #status
    staffID = db.Column(db.String(10), db.ForeignKey('staff.staffID'), nullable=False)

    staff = db.relationship('Staff', backref=db.backref('sales', lazy=True))
