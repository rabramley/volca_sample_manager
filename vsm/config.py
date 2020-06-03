import os
from dotenv import load_dotenv

# Load environment variables from '.env' file.
load_dotenv()


class BaseConfig(object):
    TESTING = os.getenv("TESTING", "False") == 'True'

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "False") == 'True'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ["SECRET_KEY"]

    SQLALCHEMY_DATABASE_URI = os.environ["DB_URI"]
    PRINTING_SET_SLEEP=2

    FILE_UPLOAD_DIRECTORY = os.environ["FILE_UPLOAD_DIRECTORY"]

    CELERY_BROKER_URL = os.environ["CELERY_BROKER_URL"]
    CELERY_RESULT_BACKEND = os.environ["CELERY_RESULT_BACKEND"]


class TestConfig(BaseConfig):
    """Configuration for general testing"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ECHO = False
    FILE_UPLOAD_DIRECTORY = os.path.join(BaseConfig.BASE_DIR, "tests", "file_uploads")


class TestConfigCRSF(TestConfig):
    WTF_CSRF_ENABLED = True
