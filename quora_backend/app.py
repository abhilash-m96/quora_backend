from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager, get_jwt_claims

from resources.user import UserResource, UserByUsername, UserList, UserLogin
from resources.question import QuestionResource, QuestionList
from resources.answer import AnswerResource, AnswerList
from resources.comment import CommentResource, CommentList

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "abhi"
api = Api(app)

jwt = JWTManager(app)

"""
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:  # first user
        return {"is_admin": True}
    return {"is_admin": False}
"""
# use the above for delete operations in resources
# as shown below

"""
@jwt_required
def delete(self, name):
    claims = get_jwt_claims()
    if not claims.get("is_admin"):
        return {"message": "Admin privilege required"}, 401
"""


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(UserList, "/users")
api.add_resource(UserResource, "/user", methods=["POST"])
api.add_resource(UserByUsername, "/user/<string:username>")
api.add_resource(QuestionResource, "/question")
api.add_resource(QuestionList, "/questions")
api.add_resource(AnswerResource, "/answer")
api.add_resource(AnswerList, "/answers")
api.add_resource(CommentResource, "/comment")
api.add_resource(CommentList, "/comments")
api.add_resource(UserLogin, "/login")

if __name__ == "__main__":
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
