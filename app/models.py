from . import db
from enum import Enum
import os
import datetime

class LeaveStatus(Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    pswd_hash = db.Column(db.String(64), nullable=False)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    publisher = db.Column(db.String(50), nullable=False)
    type=db.Column(db.Enum(), nullable=False)
    time = db.Column(db.DateTime, nullable=False)

class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.String(12), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    tel = db.Column(db.String(12))
    department = db.Column(db.String(255))
    role_in_depart = db.Column(db.String(255))
    pswd_hash = db.Column(db.String(64), nullable=False)
    id = db.Column(db.Integer, primary_key=True)

class LeaveApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(50), nullable=False)
    student_name = db.Column(db.String(50))
    student_department = db.Column(db.String(255))
    status = db.Column(db.Enum(LeaveStatus), default=LeaveStatus.PENDING)
    reason = db.Column(db.String(255), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
