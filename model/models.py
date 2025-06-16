from controllers.database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer,autoincrement=True,primary_key = True)
    user_name = db.Column(db.String(45),nullable=False)
    email = db.Column(db.String(45),nullable=False)
    password = db.Column(db.String(45),nullable=False)
    address = db.Column(db.String(50),nullable=False)
    pincode = db.Column(db.Integer,nullable=False)
class Admin(db.Model):
    __tablename__='admin'
    admin_id= db.Column(db.Integer,autoincrement=True,primary_key = True)
    admin_name = db.Column(db.String(45),nullable=False)
    email = db.Column(db.String(45),nullable=False)
    password = db.Column(db.String(45),nullable=False)

class Parkinglot(db.Model):
    __tablename__ = 'parkinglot'
    lot_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    location = db.Column(db.String(45),nullable=False)
    price = db.Column(db.Integer,nullable=False)
    address = db.Column(db.String(50),nullable=False)
    pincode = db.Column(db.Integer,nullable=False)
    max_spots = db.Column(db.Integer,nullable=False)

class Parkingspot(db.Model):
    __tablename__='parkingspot'
    spot_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    status = db.Column(db.String,nullable=False)
    lot_id = db.Column(db.Integer,db.ForeignKey('parkinglot.lot_id'),nullable=False)

class Registeredspot(db.Model):
    __tablename__ = 'registeredspot'
    registration_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    registered_spot_id = db.Column(db.Integer,db.ForeignKey('parkingspot.spot_id'),nullable=False)
    registered_user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False)
    parking_timestamp = db.Column(db.DateTime, default=lambda: datetime.now())
    leaving_timestamp = db.Column(db.DateTime, nullable=True)
    vehicle_no  = db.Column(db.String(12),nullable=False)
    cost_per_hour = db.Column(db.Integer,nullable=False)