import os

basedir = os.path.abspath(os.path.dirname(__file__))

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "U can use os.urandom(32) to generate random key"
    )
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.googlemail.com")
    MAIL_PORT = int(
        os.environ.get("MAIL_PORT", "587")
    )  # 587 for TLS=true, 465 for SSL=True
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() in ["true", "on", "1"]
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", "false")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    FLASKY_MAIL_SUBJECT_PREFIX = "[admin_from_kwesan_sys]"
    FLASKY_MAIL_SENDER = "Viem Trieu <bluitdev@gmail.com>"
    FLASKY_ADMIN = os.environ.get("FLASKY_ADMIN", "trieu_vinh_viem")
    RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    ENV = os.environ.get("ENV", "development")
    DEBUG = True
    TESTING = True  # use for on/off recaptcha
    # use for enable/disable google recaptcha, if TRUE, then ignore check captcha
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
        "SQLALCHEMY_TRACK_MODIFICATIONS", True
    )
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DEV_DATABASE_URL")
        or "postgresql+psycopg2://postgres:P@ssword@localhost:5455/quizdb"
    )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or "sqlite://"
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
        "SQLALCHEMY_TRACK_MODIFICATIONS", False
    )
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class HerokuConfig(ProductionConfig):
    SSL_REDIRECT = True if os.environ.get("DYNO") else False

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle reverse proxy server headers
        from werkzeug.contrib.fixers import ProxyFix

        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler

        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


class DockerConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler

        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "heroku": HerokuConfig,
    "docker": DockerConfig,
    "default": DevelopmentConfig,
}