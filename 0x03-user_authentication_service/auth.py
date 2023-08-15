#!/usr/bin/env python3
"""Module contains a _hash_password function"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password and returns the bytes object"""
    encoded_pass = password.encode('utf-8')
    salt = bcrypt.gensalt(len(password))
    hashed_pass = bcrypt.hashpw(encoded_pass, salt)
    return hashed_pass
