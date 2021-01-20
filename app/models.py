from extensions import db, bcrypt
import enum, datetime


class RoleType(enum.Enum):
    ADMI = "Administrator"
    STUD = "Student"
    LECT = "Lecturer"


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.Unicode(15), index=True, nullable=False)
    lastname = db.Column(db.Unicode(35), index=False, nullable=False)
    username = db.Column(db.String(80), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(60), index=False, nullable=False)
    major = db.Column(db.Unicode(50), index=False, nullable=False)
    aboutuser = db.Column(db.Unicode(100), index=False, nullable=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )
    role = db.Column(db.Enum(RoleType), index=True, nullable=False)
    confirmed = db.Column(db.Boolean, default=False, nullable=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    questions = db.relationship("Question", backref="user_questions", lazy=True)

    def __init__(
        self, firstname, lastname, username, email, password, major, aboutuser, role
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

    def __repr__(self):
        return "<User {} {}>".format(self.username, self.role)


userAnswer = db.Table(
    "useranswers",
    db.Column("userid", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("questionid", db.Integer, db.ForeignKey("questions.id"), primary_key=True),
    db.Column(
        "questionsetid", db.Integer, db.ForeignKey("questionsets.id"), primary_key=True
    ),
    db.Column("choice_id_of_user", db.Integer, nullable=True),
    db.Column("corrected", db.Boolean, nullable=True),
)


class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Unicode, nullable=False)
    field = db.Column(db.Unicode, nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    choices = db.relationship("Choice", backref="question_choices", lazy=True)
    useranswers = db.relationship(
        "User",
        secondary=userAnswer,
        lazy="subquery",
        backref=db.backref("question_user_answer", lazy=True),
    )


class Choice(db.Model):
    __tablename__ = "choices"
    id = db.Column(db.Integer, primary_key=True)
    choice_content = db.Column(db.Unicode, nullable=False, index=True)
    is_correct = db.Column(db.Boolean, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)


class QuestionSet(db.Model):
    __tablename__ = "questionsets"
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    num_of_question = db.Column(db.SmallInteger, nullable=False)
    list_question_id = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.SmallInteger, nullable=False)
    active_code = db.Column(db.String(64), nullable=False)


userParticipate = db.Table(
    "participates",
    db.Column("userid", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column(
        "questionsetid", db.Integer, db.ForeignKey("questionsets.id"), primary_key=True
    ),
    db.Column("started_time", db.DateTime, server_default=db.func.now()),
    db.Column("finished_time", db.DateTime, nullable=True),
    db.Column("result", db.Float, nullable=True, default=0),
)
