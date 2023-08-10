#!/usr/bin/env python3
"""Module contains a SessionDBAuth class
That inherits from SessionExpAuth class"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import uuid
from datetime import datetime, timedelta
from models.base import DATA


class SessionDBAuth(SessionExpAuth):
    """A Data base stored session class"""
    def create_session(self, user_id=None) -> str:
        """Creates a session"""
        if user_id is None:
            return None
        if type(user_id) not in [str]:
            return None
        session_id = str(uuid.uuid4())
        user_session = UserSession(session_id=session_id, user_id=user_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """Returns a user_id based on a session_id"""
        if session_id is None:
            return None
        if 'UserSession' not in DATA:
            return None
        user_sessions = UserSession.search({"session_id": session_id})
        if len(user_sessions) == 0:
            return None
        user_session = user_sessions[0]
        user_id = user_session.user_id
        created_at = user_session.created_at

        if self.session_duration <= 0:
            return user_id
        if not created_at:
            return None

        time_delta = timedelta(seconds=self.session_duration)
        if (created_at + time_delta) < datetime.now():
            return None
        return user_id

    def destroy_session(self, request=None):
        """Deletes the User session / logout"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if 'UserSession' not in DATA:
            return False
        user_sessions = UserSession.search({"session_id": session_id})
        if len(user_sessions) == 0:
            return False
        user_session = user_sessions[0]
        user_session.remove()
        return True
