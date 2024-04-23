import os
from datetime import datetime, timezone, timedelta

import jwt
from flask import request, Response, json, Blueprint, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

from src import User, bcrypt, db, mail

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


s = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))


@users.route('/forgot-password', methods=["POST"])
def forgot_password():
    try:
        data = request.get_json()
        email = data.get('email')
        if email:
            user = User.query.filter_by(email=email).first()
            if user:
                token = s.dumps(email, salt='reset-password')

                link = url_for('api.users.reset_password', token=token, _external=True)

                subject = "Redefinição de Senha"
                recipients = [email]
                body = f'Para redefinir sua senha, clique no seguinte link: {link}'
                sender = 'hi@demomailtrap.com'

                msg = Message(subject, recipients=recipients, body=body, sender = sender)
                mail.send(msg)

                return Response(
                    response=json.dumps({'status': 'success', "message": "E-mail de redefinição de senha enviado."}),
                    status=200,
                    mimetype='application/json'
                )
            else:
                return Response(
                    response=json.dumps({'status': 'failed', "message": "E-mail não encontrado."}),
                    status=404,
                    mimetype='application/json'
                )
        else:
            return Response(
                response=json.dumps({'status': 'failed', "message": "E-mail é necessário."}),
                status=400,
                mimetype='application/json'
            )
    except Exception as e:
        return Response(
            response=json.dumps({'status': "failed", "message": "Erro ocorrido", "error": str(e)}),
            status=500,
            mimetype='application/json'
        )


@users.route('/reset-password/<token>', methods=["POST"])
def reset_password(token):
    try:
        data = request.get_json()
        new_password = data.get('password')
        if new_password:
            email = s.loads(token, salt='reset-password', max_age=3600)  # Token válido por 1 hora
            user = User.query.filter_by(email=email).first()
            if user:
                user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                db.session.commit()

                return Response(
                    response=json.dumps({'status': 'success', "message": "Senha redefinida com sucesso."}),
                    status=200,
                    mimetype='application/json'
                )
            else:
                return Response(
                    response=json.dumps({'status': 'failed', "message": "Usuário não encontrado."}),
                    status=404,
                    mimetype='application/json'
                )
        else:
            return Response(
                response=json.dumps({'status': 'failed', "message": "Nova senha é necessária."}),
                status=400,
                mimetype='application/json'
            )
    except (SignatureExpired, BadSignature):
        return Response(
            response=json.dumps({'status': 'failed', "message": "Token inválido ou expirado."}),
            status=400,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            response=json.dumps({'status': "failed", "message": "Erro ocorrido", "error": str(e)}),
            status=500,
            mimetype='application/json'
        )
