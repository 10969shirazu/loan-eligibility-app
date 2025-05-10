from app import db


class LoanRequest(db.Model):
    __tablename__ = 'loan_request'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    loan_amnt = db.Column(db.Float)
    term = db.Column(db.Integer)
    annual_inc = db.Column(db.Float)
    int_rate = db.Column(db.Float)
    emp_length = db.Column(db.String(20))
    home_ownership = db.Column(db.String(20))
    verification_status = db.Column(db.String(20))
    purpose = db.Column(db.String(50))
    dti = db.Column(db.Float)
    delinq_2yrs = db.Column(db.Integer)
    inq_last_6mths = db.Column(db.Integer)
    open_acc = db.Column(db.Integer)
    pub_rec = db.Column(db.Integer)
    revol_bal = db.Column(db.Float)
    revol_util = db.Column(db.Float)
    total_acc = db.Column(db.Integer)
    last_pymnt_amnt = db.Column(db.Float)
    result = db.Column(db.String(20))
    reason = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())