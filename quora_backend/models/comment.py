from datetime import datetime
from db import db


class CommentModel(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(500), nullable=False)

    answer_id = db.Column(db.Integer, db.ForeignKey("answers.id"), nullable=False)
    answer = db.relationship("AnswerModel", lazy=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel", lazy=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, comment, answer_id, user_id):
        self.comment = comment
        self.answer_id = answer_id
        self.user_id = user_id

    def json(self):
        return {"id": self.id, "answer_id": self.answer_id, "comment": self.comment}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_comment_by_id(cls, _id):
        return cls.query.filter_by(id=_id)

    @classmethod
    def get_comments_by_answer_id(cls, answer_id):
        return cls.query.filter(cls.answer_id == answer_id).all()

    def __repr__(self):
        return f"Comment('{self.id}, '{self.created_at}')"
