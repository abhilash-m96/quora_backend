from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)  # max 100 chars
    full_name = db.Column(db.String(40), nullable=False)  # max 100 chars
    questions = db.relationship("QuestionModel", lazy="dynamic")

    def __init__(self, username, password, email, full_name):
        self.username = username
        self.password = password
        self.email = email
        self.full_name = full_name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "questions": [question.json() for question in self.questions.all()],
        }
