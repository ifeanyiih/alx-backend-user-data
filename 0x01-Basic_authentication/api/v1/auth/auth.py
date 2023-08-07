#!/usr/bin/env python3
"""Module contains the Auth class
for Authentication purposes"""
from typing import TypeVar, List
from flask import request


class Auth:
    """Template for all authentication systems"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns False for now"""
        return False

    def authorization_header(self, request=None) -> str:
        """Returns None"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None"""
        return None
