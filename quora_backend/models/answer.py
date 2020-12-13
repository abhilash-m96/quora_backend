from datetime import datetime
from db import db


class AnswerModel(db.Model):
    __tablename__ = "answers"
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(2000), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel", lazy=True)

    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    question = db.relationship("QuestionModel")

    comments = db.relationship("CommentModel", lazy="dynamic")

    def __init__(self, answer, question_id, user_id):
        self.answer = answer
        self.question_id = question_id
        self.user_id = user_id

    def json(self):
        return {
            "id": self.id,
            "question_id": self.question_id,
            "answer": self.answer,
            "comments": [comment.json() for comment in self.comments.all()],
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_answer_by_id(cls, _id):
        return cls.query.filter_by(id=_id)

    @classmethod
    def get_answers_by_question_id(cls, question_id):
        return cls.query.filter(cls.question_id == question_id).all()

    def __repr__(self):
        return f"Answer('{self.id}, '{self.created_at}')"
