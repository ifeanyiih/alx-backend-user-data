#!/usr/bin/env python3
"""Module of SessionAuth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, g
from models.user import User
from models.base import DATA
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def handleLogin() -> str:
    """POST /api/v1/auth_session/login
    Return:
    - a dictionary representing the loggedin user
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not len(email):
        return jsonify({"error": "email missing"}), 400

    if not password or not len(password):
        return jsonify({"error": "password missing"}), 400

    if 'User' not in DATA:
        return jsonify({"error": "no user found for this email"}), 404
    user_list = User.search({"email": email})
    if len(user_list) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    for user in user_list:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session = auth.create_session(user.id)
            session_name = getenv('SESSION_NAME')
            response = jsonify(user.to_json())
            response.set_cookie(session_name, session)
            return response, 200
    return jsonify({"error": "wrong password"}), 401
