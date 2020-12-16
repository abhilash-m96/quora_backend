from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from werkzeug.security import safe_str_cmp


class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "email", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "full_name", type=str, required=True, help="This field cannot be blank."
    )

    def get(self, id: int):
        user = UserModel.find_by_id(id)
        if user:
            return user.json()
        return {"message": "User not found"}, 404

    def post(self):
        data = UserResource.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(
            data["username"], data["password"], data["email"], data["full_name"]
        )
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class UserByUsername(Resource):
    def get(self, username: str):
        user = UserModel.find_by_username(username)
        if user:
            return user.json()
        return {"message": "User not found"}, 404


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be blank."
    )

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()

        user = UserModel.find_by_username(data["username"])
        if user and safe_str_cmp(user.password, data["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": "Invalid credentials"}, 401


class UserList(Resource):
    @jwt_required
    def get(self):
        return {"users": list(map(lambda x: x.json(), UserModel.query.all()))}
