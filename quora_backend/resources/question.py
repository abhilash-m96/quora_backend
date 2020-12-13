from flask_restful import Resource, reqparse
from models.question import QuestionModel


class QuestionResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "question", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "user_id", type=int, required=True, help="Every question needs a user_id."
    )

    def get(self, _id):
        question = QuestionModel.find_by_id(_id)
        if question:
            return user.json()
        return {"message": "User not found"}, 404

    def post(self):
        data = QuestionResource.parser.parse_args()

        if QuestionModel.find_by_question_text(data["question"]):
            return {"message": "Question already exists"}, 400

        question = QuestionModel(data["question"], data["user_id"])
        question.save_to_db()

        return {"message": "Question posted successfully."}, 201


class QuestionByQuestionText(Resource):
    def get(self, question):
        question = QuestionModel.find_by_question_text(question)
        if question:
            return question.json()
        return {"message": "No results found"}


class QuestionList(Resource):
    def get(self):
        return {"questions": list(map(lambda x: x.json(), QuestionModel.query.all()))}
