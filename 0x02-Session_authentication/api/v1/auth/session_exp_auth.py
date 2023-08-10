#!/usr/bin/env python3
"""Module contains a SessionAuth class
That Inherits from Auth Class"""
from .session_auth import SessionAuth
import uuid
from models.user import User
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """An Expiring Session Auth Class"""
    def __init__(self):
        """Initializes the class"""
        session_duration = getenv('SESSION_DURATION')
        if not session_duration:
            self.session_duration = 0
        elif session_duration:
            try:
                self.session_duration = int(session_duration)
            except ValueError as e:
                self.session_duration = 0

    def create_session(self, user_id=None) -> str:
        """Creates a Session"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """Returns a user_id based on a sessionID"""
        if session_id is None:
            return None
        session_dictionary = self.user_id_by_session.get(session_id)
        if not session_dictionary:
            return None
        user_id = session_dictionary.get("user_id")
        created_at = session_dictionary.get("created_at")
        if self.session_duration <= 0:
            return user_id
        if not created_at:
            return None

        time_delta = timedelta(seconds=self.session_duration)
        if (created_at + time_delta) < datetime.now():
            return None
        return user_id
