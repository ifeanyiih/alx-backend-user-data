#!/usr/bin/env python3
"""Module contains a BasicAuth class"""
import base64
from .auth import Auth
from models.user import User
from typing import List, TypeVar


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
            try:
                utf8_decode = decoded.decode('utf-8')
            except UnicodeDecodeError:
                return None
            else:
                return utf8_decode

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

    def user_object_from_credentials(
                self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """returns a User instance based on email and password"""
        if type(user_email) not in [str] or user_email is None:
            return None
        if type(user_pwd) not in [str] or user_pwd is None:
            return None
        users = User.search({"email": user_email})
        if len(users) == 0:
            return None
        user = None
        for user_ in users:
            if user_.is_valid_password(user_pwd):
                user = user_
                break
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Overloads Auth and retrieves
        the User instance for a request"""
        authorization_header = self.authorization_header(request)
        base64_extract = self.extract_base64_authorization_header(
                                                    authorization_header)
        base64_decode = self.decode_base64_authorization_header(base64_extract)
        user_cred_extract = self.extract_user_credentials(base64_decode)
        user = self.user_object_from_credentials(*user_cred_extract)
        return user
