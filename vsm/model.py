from datetime import datetime
from vsm.database import db


class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True, unique=True)
    filename = db.Column(db.String(500), nullable=False)
    created_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)


class Bank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True, unique=True)
    filename = db.Column(db.String(500), nullable=False)
    created_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
