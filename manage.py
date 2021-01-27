from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_bcrypt import Bcrypt
import datetime

from app import db
from run import app
from app.models import User, RoleType

migrate = Migrate(app, db)
manager = Manager(app)


@manager.command
def create_admin():
    db.session.add(
        User(
            firstname="Viem",
            lastname="Trieu Vinh",
            username="tvviem",
            email="tvviem@blu.edu.vn",
            password="pass123",
            major="it-admin",
            aboutuser="Ham muốn làm ra ứng dụng",
            role=RoleType.ADMI,
            confirmed=True,
            confirmed_on=datetime.datetime.now(),
        )
    )
    db.session.commit()


manager.add_command("db", MigrateCommand)


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


if __name__ == "__main__":
    manager.run()