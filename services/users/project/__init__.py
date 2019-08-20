import os

from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

# instantiate the app
app = Flask(__name__)

api = Api(app)


# set config
app_settings = os.getenv("APP_SETTINGS")
app.config.from_object(app_settings)

# instantiate the db
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, username, phone_number):
        self.username = username
        self.phone_number = phone_number


class UsersPing(Resource):
    def get(self):
        return {"status": "success", "message": "pong!"}


api.add_resource(UsersPing, "/users/ping")

