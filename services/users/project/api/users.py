import re
from flask import Blueprint, request, render_template
from flask_restful import Resource, Api
from sqlalchemy import exc
from project import db
from project.api.models import User

users_blueprint = Blueprint("users", __name__, template_folder="./templates")
api = Api(users_blueprint)


def validate_phone(value):
    numbers = re.findall(r"\(?\d{3}\)?-?.?\s?\d{3}\s?-?\s?.?\s?\d{4}", value)
    numbers_list = list(numbers)

    clean_list = []
    for obj in numbers_list:
        clean_list.append(re.sub(r"\(?\)?\.?-?", "", obj))

    formatted_list = []
    for obj in clean_list:
        try:
            int(obj)
            area_code = obj[0:3]
            line_prefix = obj[3:6]
            line_number = obj[6:10]

            formatted_list.append(f"({area_code}) {line_prefix}-{line_number}")

        except ValueError:
            continue

    return formatted_list


# our view
@users_blueprint.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        phone_number = request.form["phone_number"]
        clean_phone_number = validate_phone(phone_number)

        for obj in clean_phone_number:
            db.session.add(User(username=username, phone_number=obj))
            db.session.commit()
    users = User.query.all()

    return render_template("index.html", users=users)


class UsersList(Resource):
    def post(self):
        post_data = request.get_json()

        # data validation
        response_object = {"status": "fail", "message": "Invalid payload."}
        if not post_data:
            return response_object, 400

        username = post_data.get("username")
        phone_number = post_data.get("phone_number")
        try:
            user = User.query.filter_by(phone_number=phone_number).first()
            if not user:
                db.session.add(User(username=username, phone_number=phone_number))
                db.session.commit()
                response_object["status"] = "success"
                response_object["message"] = f"{username} was added!"
                return response_object, 201
            else:
                response_object["message"] = "Sorry. That username already exists."
                return response_object, 400
        except exc.IntegrityError:
            db.session.rollback()
            return response_object, 400

    def get(self):
        """Get all users"""
        response_object = {
            "status": "success",
            "data": {"users": [user.to_json() for user in User.query.all()]},
        }

        return response_object, 200


# similar to a Django detail view
class Users(Resource):
    def get(self, user_id):
        """Get single user details"""
        response_object = {"status": "fail", "message": "User does not exist"}
        try:
            user = User.query.filter_by(id=int(user_id)).first()
            if not user:
                return response_object, 404
            else:
                response_object = {
                    "status": "success",
                    "data": {
                        "id": user.id,
                        "username": user.username,
                        "phone_number": user.phone_number,
                        "active": user.active,
                    },
                }
                return response_object, 200

        except ValueError:
            return response_object, 404


class UsersPing(Resource):
    def get(self):
        return {"status": "success", "message": "pong!"}


# add it to the API
api.add_resource(UsersList, "/users")
api.add_resource(Users, "/users/<user_id>")
api.add_resource(UsersPing, "/users/ping")