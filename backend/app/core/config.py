# config.py

from dotenv import load_dotenv
from decouple import config
import os

load_dotenv()  


SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM', default='HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = config('ACCESS_TOKEN_EXPIRE_MINUTES', default=30, cast=int)
"""
This module contains the configuration settings for the application.

Attributes:
    SQLALCHEMY_DATABASE_URL (str): The URL of the SQLAlchemy database.
    SECRET_KEY (str): The secret key used for encryption.
    ALGORITHM (str): The algorithm used for token encryption.
    ACCESS_TOKEN_EXPIRE_MINUTES (int): The expiration time for access tokens in minutes.
"""
