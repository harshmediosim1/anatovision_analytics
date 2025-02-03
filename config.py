#Python Import

#Flask Import

#App Import

#Third-Party Import
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

'''The `Config` class defines configuration settings for a Python application, including a secret key,
database URI, and modification tracking setting.'''
# class Config:
#     SECRET_KEY = os.getenv("SECRET_KEY")
#     SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///analytics.db")
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Max upload size (16MB)
#     UPLOAD_FOLDER = 'uploads/'


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

