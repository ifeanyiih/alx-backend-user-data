#!/usr/bin/env python3
"""Module contains a BasicAuth class"""
import base64
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

    def decode_base64_authorization_header(
                            self, base64_authorization_header: str) -> str:
        """Returns the decoded value of a Base64 string"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) not in [str]:
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
        except base64.binascii.Error as e:
            return None
        else:
            return decoded.decode('utf-8')

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Returns the user email and password form the Base64
        decoded value"""
        decoded = decoded_base64_authorization_header
        if decoded is None:
            return None, None
        if type(decoded) not in [str]:
            return None, None
        if ':' not in decoded:
            return None, None
        return decoded.split(':')[0], decoded.split(':')[1]
