from extensions import db, bcrypt
from flask_login import UserMixin
import enum, datetime


class RoleType(enum.Enum):
    ADMI = "Administrator"
    STUD = "Student"
    LECT = "Lecturer"


class User(UserMixin, db.Model):
    __tablename__ = "users"
    # if you want to identify a specific schema, you can use the below command
    # notice: before making newschema
    # __table_args__ = {"schema": "newschema"}
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.Unicode(15), index=True, nullable=False)
    lastname = db.Column(db.Unicode(35), index=False, nullable=False)
    username = db.Column(db.String(80), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(80), index=False, nullable=False)
    major = db.Column(db.Unicode(50), index=False, nullable=False)
    aboutuser = db.Column(db.Unicode(100), index=False, nullable=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )
    role = db.Column(db.Enum(RoleType), index=True, nullable=False, default=RoleType.STUD)
    confirmed = db.Column(db.Boolean, default=False, nullable=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    # backref "user_questions" use for referencing to the user when create any questions
    questions = db.relationship(
        "Question", backref="user_questions", lazy="dynamic"
    )  # dynamic for more filter, count, ...
    # for example: when create question we can use command
    # user = User(firstname="alice",....)
    # question = Question(...,..., user_questions = user) # user_questions is used here
    useranswers = db.relationship("UserAnswer", backref="user_answer", lazy="select")
    questionsets = db.relationship("UserParticipate", back_populates="user")

    def __init__(
        self,
        firstname,
        lastname,
        username,
        email,
        password,
        major,
        aboutuser,
        role,
        confirmed=False,
        confirmed_on=None,
    ):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        # decode to ensure that our passwords are stored in db with proper character encoding
        self.password = bcrypt.generate_password_hash(password).decode("UTF-8")
        self.major = major
        self.aboutuser = aboutuser
        self.role = role
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("UTF-8")

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password=password)

    def is_admin(self):
        return self.role == RoleType.ADMI

    def is_lecturer(self):
        return self.role == RoleType.LECT

    def is_student(self):
        return self.role == RoleType.STUD

    def __repr__(self):  # use for representing object when printed
        return "{} {}".format(self.lastname, self.firstname)


class UserAnswer(db.Model):
    __tablename__ = "useranswers"
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    question_id = db.Column(
        db.Integer, db.ForeignKey("questions.id", ondelete="CASCADE"), primary_key=True
    )
    questionset_id = db.Column(
        db.Integer, db.ForeignKey("questionsets.id"), primary_key=True
    )
    chosen_id_from_user = db.Column(db.Integer, nullable=True)
    is_right = db.Column(db.Boolean, nullable=True)


class Field(db.Model):
    __tablename__ = "fields"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False, unique=True)
    questions = db.relationship("Question", backref="field_questions", lazy="dynamic")


class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Unicode, nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )
    field_id = db.Column(
        db.Integer, db.ForeignKey("fields.id", ondelete="CASCADE"), nullable=False
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    choices = db.relationship("Choice", backref="question_choices", lazy="joined")
    # Consider about executing time: lazy = dynamic < select < joined < subquery
    # because: 1/ 'dynamic' and 'select' exe seperate query, moreover; dynamic use for filter, orderby, count...
    # 2/ 'joined' and 'subquery' will get all data in once calling query

    question_answered = db.relationship(
        "UserAnswer", backref="question_answered", lazy="select"
    )


class Choice(db.Model):
    __tablename__ = "choices"
    id = db.Column(db.Integer, primary_key=True)
    choice_content = db.Column(db.Unicode, nullable=False, index=True)
    is_correct = db.Column(db.Boolean, nullable=False)
    question_id = db.Column(
        db.Integer, db.ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )

    def __init__(self, choice_content, is_correct):
        self.choice_content = choice_content
        self.is_correct = is_correct


class QuestionSet(db.Model):
    __tablename__ = "questionsets"
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    num_of_days = db.Column(db.SmallInteger, default=1, nullable=False)
    describe = db.Column(db.Unicode, nullable=False)
    num_of_question = db.Column(db.SmallInteger, nullable=False)
    duration = db.Column(
        db.SmallInteger, nullable=False
    )  # number of minutes to finish this test
    active_code = db.Column(
        db.String(64), nullable=False
    )  # hashed when lecturer create set of question
    list_question_id = db.Column(
        db.String(100)
    )  # symmetric encoded by system using active_code from lecturer; decoded when student provide active_code appropriately

    user_answer = db.relationship("UserAnswer", backref="questionset", lazy="select")
    users = db.relationship("UserParticipate", back_populates="questionset")

    def __init__(
        self, describe, num_of_question, duration, active_code, list_question_id
    ):
        self.describe = describe
        self.num_of_question = num_of_question
        self.duration = duration
        self.active_code = active_code
        self.list_question_id = list_question_id


class UserParticipate(db.Model):
    __tablename__ = "participates"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    questionset_id = db.Column(
        db.Integer, db.ForeignKey("questionsets.id", ondelete="CASCADE")
    )
    started_time = db.Column(db.DateTime, server_default=db.func.now())
    finished_time = db.Column(db.DateTime, nullable=True)
    result = db.Column(db.Float, nullable=True, default=0)
    user = db.relationship("User", back_populates="questionsets")
    questionset = db.relationship("QuestionSet", back_populates="users")
