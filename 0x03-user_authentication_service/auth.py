#!/usr/bin/env python3
"""Module contains a _hash_password function"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


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

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if login details validates"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound as e:
            return False
        else:
            encoded_pass = password.encode('utf-8')
            salt = bcrypt.gensalt(len(password))
            hashed_pass = bcrypt.hashpw(encoded_pass, salt)
            if bcrypt.checkpw(encoded_pass, hashed_pass):
                return True
            else:
                return False

    def create_session(self, email: str) -> str:
        """Returns a session_id as a string"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound as e:
            pass
        else:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id


def _hash_password(password: str) -> bytes:
    """Hashes a password and returns the bytes object"""
    encoded_pass = password.encode('utf-8')
    salt = bcrypt.gensalt(len(password))
    hashed_pass = bcrypt.hashpw(encoded_pass, salt)
    return hashed_pass


def _generate_uuid() -> str:
    """Generates and returns a uuid"""
    return str(uuid.uuid4())
