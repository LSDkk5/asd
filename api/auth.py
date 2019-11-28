from flask import Blueprint, request, jsonify, abort, render_template, url_for
from flask_login import login_user, current_user
from flask_restful import Resource
from datetime import datetime

from utils.token import generate_confirmation_token, confirm_token
from utils.send_email import send_email
from web.models import User
from web import bcrypt, db, api

api_auth = Blueprint('api_auth', __name__)


class Login(Resource):
    def post(self):
        loginData = {
            'username': request.json['username'],
            'password': request.json['password']}
        user = User.query.filter_by(username=loginData['username']).first()
        if user and bcrypt.check_password_hash(
            user.password, loginData['password']):
            login_user(user)
        else:
            return abort(401, description='Dane logowania są niepoprawne! Spradz poprawność wprowadzonych danych!')
        return jsonify(message='Zostałeś pomyślnie zalogowany do serwisu!')

class Register(Resource):
    def post(self):
        registerData = {
            'username': request.json['username'],
            'password': request.json['password'],
            'email': request.json['email']}
        user = User.query.filter_by(username=registerData['username']).first()
        userEmail = User.query.filter_by(email=registerData['email']).first()

        if user:
            return abort(403, description='Użytkownik o podanej nazwie już istnieje!')
        elif userEmail:
            return abort(403, description='Konto o podanym adresie email już istnieje! prosimy o podanie innego.')
        newUser = User(
            username=registerData['username'],
            password=bcrypt.generate_password_hash(
                registerData['password']),
            email=registerData['email'],
            registered_on=datetime.now())
        token = generate_confirmation_token(newUser.email)
        db.session.add(newUser)
        send_email(
            newUser.email,
            'Aktywacja Konta',
            render_template(
                'auth/activate.html',
                confirm_url=url_for(
                    'auth.confirm_account',
                    token=token,
                    _external=True)))
        db.session.commit()
        return jsonify(message='Twoje konto zostało pomyślnie utworzone! Na adres e-mail została wysłana wiadomość z linkiem aktywacyjnym - prosimy aktywować konto.')

api.add_resource(Login, '/api/v1.0/auth/login')
api.add_resource(Register, '/api/v1.0/auth/register')






# @api_auth.route('/api/login', methods=['POST'])
# def login_controller():
#     loginData = {
#         'username': request.json['username'],
#         'password': request.json['password']}
#     user = User.query.filter_by(username=loginData['username']).first()
#     if user and bcrypt.check_password_hash(
#             user.password, loginData['password']):
#         login_user(user)
#     else:
#         return jsonify(403)
#     return jsonify(200)


# @api_auth.route('/api/register', methods=['POST'])
# def register_controller():
#     registerData = {
#         'username': request.json['username'],
#         'password': request.json['password'],
#         'email': request.json['email']}
#     user = User.query.filter_by(username=registerData['username']).first()
#     userEmail = User.query.filter_by(email=registerData['email']).first()

#     if user:
#         return jsonify(403, description='Użytkownik o podanej nazwie już istnieje!')
#     elif userEmail:
#         return abort(403, description='Konto o podanym adresie email już istnieje! prosimy o podanie innego.')
#     newUser = User(
#         username=registerData['username'],
#         password=bcrypt.generate_password_hash(
#             registerData['password']),
#         email=registerData['email'],
#         registered_on=datetime.now())
#     db.session.add(newUser)
#     db.session.commit()

#     token = generate_confirmation_token(newUser.email)
#     return jsonify(200, token)


# @api_auth.route('/api/account/confirm/<token>')
# def confirm_account_controller(token):
#     try:
#         email = confirm_token(token)
#     except BaseException:
#         return jsonify(403)
#     user = User.query.filter_by(email=email).first_or_404()
#     if user.confirmed:
#         return jsonify(403)
#     else:
#         user.confirmed = True
#         db.session.commit()
#     return jsonify(200)


# @api_auth.route('/api/resend/token', methods=['POST'])
# def resend_confirm_token():
#     if current_user.is_authenticated:
#         if not current_user.confirmed:
#             user = User.query.filter_by(
#                 username=current_user.username).first_or_404()
#             token = generate_confirmation_token(user.email)
#             send_email(to=user.email, subject='test', template=token)
#     else:
#         return jsonify(404)


# @api_auth.route('/api/password/forget', methods=['POST'])
# def forget_password_controller():
#     email = request.json['email']
#     user = User.query.filter_by(email=email).first()
#     if not user:
#         return jsonify(403)
#     token = generate_confirmation_token(email)
#     return jsonify(token)


# @api_auth.route('/api/password/r<token>', methods=['POST'])
# def reset_password_controller(token):
#     newPassword = request.json['password']
#     try:
#         email = confirm_token(token)
#     except BaseException:
#         return jsonify(403)

#     user = User.query.filter_by(email=email).first_or_404()
#     user.password = bcrypt.generate_password_hash(newPassword)
#     db.session.commit()
#     return jsonify(200)