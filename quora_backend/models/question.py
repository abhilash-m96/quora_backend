from db import db
from datetime import datetime


class QuestionModel(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    answers = db.relationship("AnswerModel", lazy="dynamic")

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("UserModel")

    def __init__(self, question, user_id):
        self.question = question
        self.user_id = user_id

    def json(self):
        return {
            "id": self.id,
            "question": self.question,
            "answers": [answer.json() for answer in self.answers.all()],
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_question_text(cls, question):
        return cls.query.filter_by(question=question).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
