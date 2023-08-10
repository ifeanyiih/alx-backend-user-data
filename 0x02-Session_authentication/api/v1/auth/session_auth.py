#!/usr/bin/env python3
"""Module contains a SessionAuth class
That Inherits from Auth Class"""
from .auth import Auth
import uuid


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
