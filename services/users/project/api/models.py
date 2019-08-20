from sqlalchemy.sql import func

from project import db


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, username, phone_number):
        self.username = username
        self.phone_number = phone_number

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "phone_number": self.phone_number,
            "active": self.active,
        }
