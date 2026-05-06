from app.routes.extensions import db
from datetime import datetime, timezone

class Voucher(db.Model):
    __tablename__ = 'vouchers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    total = db.Column(db.Numeric(10, 4), nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)

    items = db.relationship('VoucherItem', back_populates='voucher', cascade='all, delete-orphan')

class VoucherItem(db.Model):
    __tablename__ = 'voucher_items'

    id = db.Column(db.Integer, primary_key=True)
    voucher_id = db.Column(db.Integer, db.ForeignKey('vouchers.id'), nullable=False)

    size = db.Column(db.String(15), nullable=False)
    weight = db.Column(db.Float, nullable=True)

    price = db.Column(db.Numeric(10, 4), nullable=False)
    total = db.Column(db.Numeric(10, 4), nullable=False, default=0)
    grand_total = db.Column(db.Numeric(10, 4), nullable=False, default=0)

    created_at = db.Column(db.DateTime, default=datetime.now)

    voucher = db.relationship('Voucher', back_populates='items')