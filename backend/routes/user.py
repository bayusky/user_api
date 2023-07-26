from flask import Flask, jsonify, request
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from config import ApplicationConfig
from flask_session import Session
import secrets
from mailer.mail import mailer
from .not_found import not_found


def reg_user(user_collection, request):
    _json =request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['password']

    if _name and _email and _password and request.method == 'POST':
        _hashed_password = generate_password_hash(_password)
        print(_hashed_password)
        existing_mail = user_collection.find_one({'email': _email})
        if existing_mail:
            resp = jsonify("Email exist!")
            return(resp)
        else:
            verify_token = secrets.token_urlsafe(30*3//4)
            user_collection.insert_one({'name': _name , 'email' : _email, 'password' : _hashed_password, 'verify_token': verify_token})
            flag = "register"
            mailer(_email, verify_token, flag)

            resp = jsonify("User added succesfully!")
            resp.status_code = 200

            return resp
    else:
        return not_found()