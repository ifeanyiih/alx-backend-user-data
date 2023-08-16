#!/usr/bin/env python3
"""A basic Flask app"""
from flask import Flask, jsonify, request, abort
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def rootRoute():
    """The root Route of the app"""
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """implements the POST /sessions route
    Create session cookies for users"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        abort(401)
    valid_login = AUTH.valid_login(email, password)
    if not valid_login:
        abort(401)
    session_id = AUTH.create_session(email)
    res = jsonify({"email": email, "message": "logged in"})
    res.set_cookie('session_id', session_id)
    return res, 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """Implements the POST /users route
    Adds users to the database"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
    except ValueError as e:
        return jsonify({"message": "email already registered"}), 400
    else:
        return jsonify({"email": email, "message": "user created"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
