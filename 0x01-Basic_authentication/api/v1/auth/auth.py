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
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path.endswith('/'):
            path_no_slash = path[:-1]
            exists = False

            for ex_path in excluded_paths:
                if ex_path.startswith(path) or\
                             ex_path.startswith(path_no_slash):
                    exists = True
                    break
            if exists:
                return False
            else:
                return True
        elif not path.endswith('/'):
            path_with_slash = path + '/'
            exists = False

            for ex_path in excluded_paths:
                if ex_path.startswith(path) or\
                            ex_path.startswith(path_with_slash):
                    exists = True
                    break
            if exists:
                return False
            else:
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
