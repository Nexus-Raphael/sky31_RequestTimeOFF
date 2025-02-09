from . import db

class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    pswd_hash = db.Column(db.String(64), nullable=False)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
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

class Wholeave(db.Model):
    __tablename__ = 'wholeaves'
    order = db.Column(db.Integer)
    # 修正这里的类型错误，应该是 Integer 而不是 Intrger
    id = db.Column(db.Integer, nullable=False)
    leave_reason = db.Column(db.String(255))
    check_opinion = db.Column(db.String(255))
    is_permitted = db.Column(db.Integer)
    # 修正这里的类型，应该是 db.DateTime
    check_time = db.Column(db.DateTime)
    path_to_image = db.Column(db.String(255))