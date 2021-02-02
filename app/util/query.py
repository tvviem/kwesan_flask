from ..models import User
class UserQuery(object):
    @staticmethod
    def get_user_id_by_email_or_username(email=None, username=None):
        user = User.query.filter((User.email == email) | (User.username == username)).first()
        return user.id if hasattr(user, 'id') else None

    @staticmethod
    def is_existing_email(email):
        return User.query.filter(User.email==email).first() is not None

    @staticmethod
    def is_existing_username(username):
        return User.query.filter(User.username==username).first() is not None