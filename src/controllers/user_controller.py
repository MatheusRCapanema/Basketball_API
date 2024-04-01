import os
from datetime import datetime, timezone

import jwt
from flask import request, Response, json, Blueprint

from src import User, bcrypt, db

users = Blueprint("users", __name__)


@users.route('/signup', methods=["POST"])
def handle_signup():
    try:
        data = request.get_json()
        if "firstname" in data and "lastname" and data and "email" and "password" in data:
            user = User.query.filter_by(email=data["email"]).first()
            if not user:
                user_obj = User(
                    email=data["email"],
                    firstname=data["firstname"],
                    lastname=data["lastname"],
                    password=bcrypt.generate_password_hash(data["password"]).decode('utf-8')
                )

                db.session.add(user_obj)
                db.session.commit()

                payload = {
                    'iat': datetime.now(timezone.utc),
                    'user_id': str(user_obj.id).replace('-', ""),
                    'firstname': user_obj.firstname,
                    'lastname': user_obj.lastname,
                    'email': user_obj.email,
                }
                token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
                return Response(
                    response=json.dumps({
                        'status': 'Sucesso',
                        "message": "Usuario registrado com sucesso",
                        "token": token
                    }),
                    status=201,
                    mimetype='application/json'
                )
            else:
                print(user)
                return Response(
                    response=json.dumps({'status': "Falha",
                                         "message": "User Parameters Firstname, Lastname, Email and Password are "
                                                    "required"}),
                    status=400,
                    mimetype='application/json'
                )
    except Exception as e:
        return Response(
            response=json.dumps({'status': "failed",
                                 "message": "Error Occured",
                                 "error": str(e)}),
            status=500,
            mimetype='application/json'
        )


@users.route('/signin', methods=["POST"])
def handle_login():
    try:
        data = request.json
        if "email" and "password" in data:
            user = User.query.filter_by(email=data["email"]).first()
            if user:

                if bcrypt.check_password_hash(user.password, data["password"]):

                    payload = {
                        'iat': datetime.now(timezone.utc),
                        'user_id': str(user.id).replace('-', ""),
                        'firstname': user.firstname,
                        'lastname': user.lastname,
                        'email': user.email,
                    }
                    token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
                    return Response(
                        response=json.dumps({'status': "success",
                                             "message": "User Sign In Successful",
                                             "token": token}),
                        status=200,
                        mimetype='application/json'
                    )

                else:
                    return Response(
                        response=json.dumps({'status': "failed", "message": "User Password Mistmatched"}),
                        status=401,
                        mimetype='application/json'
                    )

            else:
                return Response(
                    response=json.dumps({'status': "failed", "message": "User Record doesn't exist, kindly register"}),
                    status=404,
                    mimetype='application/json'
                )
        else:
            return Response(
                response=json.dumps({'status': "failed", "message": "User Parameters Email and Password are required"}),
                status=400,
                mimetype='application/json'
            )

    except Exception as e:
        return Response(
            response=json.dumps({'status': "failed",
                                 "message": "Error Occured",
                                 "error": str(e)}),
            status=500,
            mimetype='application/json'
        )
