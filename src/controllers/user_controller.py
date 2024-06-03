import os

from flask import request, Response, json, Blueprint, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

from src import User, bcrypt, db, mail

users = Blueprint("users", __name__)


@users.route('/signup', methods=["POST"])
def handle_signup():
    try:
        data = request.get_json()
        if "firstname" in data and "lastname" in data and "email" in data and "password" in data:
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
                return Response(
                    response=json.dumps({
                        'status': 'success',
                        "message": "User registered successfully"
                    }),
                    status=201,
                    mimetype='application/json'
                )
            else:
                return Response(
                    response=json.dumps({'status': "error", "message": "Email already registered"}),
                    status=400,
                    mimetype='application/json'
                )
    except Exception as e:
        return Response(
            response=json.dumps({'status': "error", "message": "An error occurred", "error": str(e)}),
            status=500,
            mimetype='application/json'
        )


@users.route('/signin', methods=["POST"])
def handle_login():
    try:
        data = request.get_json()
        if "email" in data and "password" in data:
            user = User.query.filter_by(email=data["email"]).first()
            if user and bcrypt.check_password_hash(user.password, data["password"]):
                return Response(
                    response=json.dumps({'status': "success", "message": "User Sign In Successful", "user_id": user.id}),
                    status=200,
                    mimetype='application/json'
                )
            elif user:
                return Response(
                    response=json.dumps({'status': "error", "message": "Incorrect password"}),
                    status=401,
                    mimetype='application/json'
                )
            else:
                return Response(
                    response=json.dumps({'status': "error", "message": "User not found, please register"}),
                    status=404,
                    mimetype='application/json'
                )
        else:
            return Response(
                response=json.dumps({'status': "error", "message": "Both email and password are required"}),
                status=400,
                mimetype='application/json'
            )
    except Exception as e:
        return Response(
            response=json.dumps({'status': "error", "message": "An error occurred", "error": str(e)}),
            status=500,
            mimetype='application/json'
        )


s = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))


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
