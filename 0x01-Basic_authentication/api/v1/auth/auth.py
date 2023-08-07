#!/usr/bin/env python3
"""Module contains the Auth class
for Authentication purposes"""
from typing import TypeVar, List
from flask import request


class Auth:
    """Template for all authentication systems"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns False for now"""
        if path is None:
            return True
        if len(excluded_paths) == 0 or excluded_paths is None:
            return True
        for ex_path in excluded_paths:
            if ex_path.startswith(path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Returns None"""
        if request is None:
            return None
        if "Authorization" not in request.headers:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None"""
        return None
