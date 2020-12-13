from flask_restful import Resource, reqparse
from models.comment import CommentModel


class CommentResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "comment", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "answer_id", type=int, required=True, help="Every answer needs a question_id."
    )
    parser.add_argument(
        "user_id", type=int, required=True, help="Every answer needs a user id"
    )

    def get(self, _id):
        answer = CommentModel.get_comment_by_id(_id)
        if answer:
            return answer.json()
        return {"message": "Comment not found"}, 404

    def post(self):
        data = CommentResource.parser.parse_args()

        comment = CommentModel(data["comment"], data["answer_id"], data["user_id"])
        comment.save_to_db()

        return {"message": "Comment posted successfully."}, 201


class CommentList(Resource):
    def get(self):
        return {"comments": list(map(lambda x: x.json(), CommentModel.query.all()))}
