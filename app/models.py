from .extensions import db
from datetime import datetime
from flask_login import UserMixin

class Enquiry(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(120))
    contact = db.Column(db.String(20))
    pickup_location = db.Column(db.String(200))
    drop_location = db.Column(db.String(200))
    country = db.Column(db.String(100), nullable=False)
    weight=db.Column(db.Float)
    estimated_price = db.Column(db.Float)
    parcel_details = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(30), default="pending")

class Shipment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    enquiry_id=db.Column(
        db.Integer,
        db.ForeignKey("enquiry.id")
    )
    name=db.Column(db.String(120))
    contact = db.Column(db.String(20))
    pickup_location = db.Column(db.String(200))
    drop_location = db.Column(db.String(200))
    country = db.Column(db.String(100))
    weight=db.Column(db.Float)
    estimated_price = db.Column(db.Float)
    parcel_details = db.Column(db.Text)
    tracking_id = db.Column(db.String(20), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(30), default="Confirmed")
   

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),unique=True,nullable=False)
    password_hash=db.Column(db.String(200),nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)

 
class CourierRate(db.Model):
        id=db.Column(db.Integer,primary_key=True)
        country=db.Column(db.String(100),unique=True,nullable=False)
        zone=db.Column(db.String(50),nullable=False)
        price_per_kg=db.Column(db.Float,nullable=False)

