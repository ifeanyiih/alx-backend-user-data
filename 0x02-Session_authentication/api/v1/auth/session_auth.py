#!/usr/bin/env python3
"""Module contains a SessionAuth class
That Inherits from Auth Class"""
from .auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """Session Authentication class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session ID for a user_id"""
        if user_id is None:
            return None
        if type(user_id) not in [str]:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a UserID based on a session ID"""
        if session_id is None:
            return None
        if type(session_id) not in [str]:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns a user instance based on a cookie value"""
        cookie_value = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie_value)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """Deletes the User session / logout"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        else:
            del self.user_id_by_session_id[session_id]
            return True
