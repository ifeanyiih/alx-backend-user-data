#!/usr/bin/env python3
"""Module contains a _hash_password function"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initializes the instance"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a User in the database"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound as e:
            hashed_pass = _hash_password(password)
            user = self._db.add_user(email, hashed_pass)
            return user
        else:
            raise ValueError(f"User {email} already exists")


def _hash_password(password: str) -> bytes:
    """Hashes a password and returns the bytes object"""
    encoded_pass = password.encode('utf-8')
    salt = bcrypt.gensalt(len(password))
    hashed_pass = bcrypt.hashpw(encoded_pass, salt)
    return hashed_pass
