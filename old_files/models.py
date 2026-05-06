from voucher.extensions import db
from datetime import datetime

# Product table
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    item_code = db.Column(db.String(50), unique=True, nullable=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    buy_price = db.Column(db.Float, nullable=False)
    sell_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    low_stock_limit = db.Column(db.Integer, nullable=False, default=5)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Product {self.name}>"

# Purchase table
class Purchase(db.Model):
    __tablename__ = 'purchases'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer, nullable=False)
    buy_price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

    product = db.relationship('Product')

# Sale table
class Sale(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    item_code = db.Column(db.String(25))
    voucher_no = db.Column(db.String(25), unique=True)
    product_name = db.Column(db.String(100))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    profit = db.Column(db.Float)
    total = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.now)
    
    product = db.relationship('Product')

# Voucher table (main invoice)
class Voucher(db.Model):
    __tablename__ = 'vouchers'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    voucher_no = db.Column(db.String(25), unique=True)
    size = db.Column(db.Integer)
    weight = db.Column(db.Float(5, 3), nullable=False)
    price = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.now)
    
    items = db.relationship('Product')

# Size table
class Size(db.Model):
    __tablename__ = 'sizes'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    size_name = db.Column(db.String(7), nullable=False)
    price = db.Column(db.Float, nullable=False)

    items = db.relationship('VoucherItem', backref="sizes")

# VoucherItem table
class VoucherItem(db.Model):
    __tablename__ = 'voucher_items'

    id = db.Column(db.Integer, primary_key=True)
    voucher_id = db.Column(db.Integer, db.ForeignKey('voucher_items.id'), nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey('sizes.id'), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
