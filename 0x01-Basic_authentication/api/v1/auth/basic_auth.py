#!/usr/bin/env python3
"""Module contains a BasicAuth class"""
from .auth import Auth


class BasicAuth(Auth):
    """Basic Authentication class"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extracts the Base64 part of the Authorization
        for Basic Authentication"""
        if authorization_header is None:
            return None
        if type(authorization_header) not in [str]:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]
