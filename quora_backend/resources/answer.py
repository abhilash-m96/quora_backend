from flask_restful import Resource, reqparse
from models.answer import AnswerModel


class AnswerResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "answer", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "question_id", type=int, required=True, help="Every answer needs a question_id."
    )
    parser.add_argument(
        "user_id", type=int, required=True, help="Every answer needs a user id"
    )

    def get(self, _id):
        answer = AnswerModel.find_by_id(_id)
        if answer:
            return answer.json()
        return {"message": "Answer not found"}, 404

    def post(self):
        data = AnswerResource.parser.parse_args()

        answer = AnswerModel(data["answer"], data["question_id"], data["user_id"])
        answer.save_to_db()

        return {"message": "Answer posted successfully."}, 201


class AnswerList(Resource):
    def get(self):
        return {"answers": list(map(lambda x: x.json(), AnswerModel.query.all()))}
