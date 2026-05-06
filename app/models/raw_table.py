from app.routes.extensions import db
from datetime import datetime


# Raw Product table
class Raw(db.Model):
    __tablename__ = 'raws'

    id = db.Column(db.Integer, primary_key=True)
    kd = db.Column(db.Integer, nullable=False)
    bag_no = db.Column(db.Integer, nullable=False)
    item_code = db.Column(db.String(50), nullable=True)
    weight = db.Column(db.Float, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Raw {self.name}>"
