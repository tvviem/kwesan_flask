from . import db
import enum

class RoleType(enum.Enum):
    ADMI = "Administrator"
    STUD = "Student"
    LECT = "Lecturer"

class User(db.Model):
    """Data model for user accounts."""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.Unicode(15), index=True, nullable=False)
    lastname = db.Column(db.Unicode(35), index=False, nullable=False)
    username = db.Column(db.String(80), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(60), index=False, nullable=False)
    major = db.Column(db.Unicode(50), index=False, nullable=False)
    aboutuser = db.Column(db.Unicode(100), index=False, nullable=True)
    role = db.Column(db.Enum(RoleType), index=True, nullable=False)

    def __init__(self, firstname, lastname, username, email, password, major, aboutuser, role):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password = password
        self.major = major
        self.aboutuser = aboutuser
        self.role = role

    def __repr__(self):
        return "<User {} {}>".format(self.username, self.role)
