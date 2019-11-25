from flask import Blueprint, request, jsonify
from flask_login import login_user, current_user
from datetime import datetime

from utils.token import generate_confirmation_token, confirm_token
from utils.send_email import send_email
from web.models import User
from web import bcrypt, db


auth_api = Blueprint('auth_api', __name__)

@auth_api.route('/api/login', methods=['POST'])
def login_controller():
    loginData = {
        'username': request.json['username'],
        'password': request.json['password']}
    user = User.query.filter_by(username=loginData['username']).first()
    if user and bcrypt.check_password_hash(
            user.password, loginData['password']):
        login_user(user)
    else:
        return jsonify(403)
    return jsonify(200)


@auth_api.route('/api/register', methods=['POST'])
def register_controller():
    registerData = {
        'username': request.json['username'],
        'password': request.json['password'],
        'email': request.json['email']}
    user = User.query.filter_by(username=registerData['username']).first()
    if user:
        return jsonify(403)
    newUser = User(
        username=registerData['username'],
        password=bcrypt.generate_password_hash(
            registerData['password']),
        email=registerData['email'],
        registered_on=datetime.utcnow())
    db.session.add(newUser)
    db.session.commit()

    token = generate_confirmation_token(newUser.email)
    return jsonify(200, token)


@auth_api.route('/api/account/confirm/<token>')
def confirm_account_controller(token):
    try:
        email = confirm_token(token)
    except BaseException:
        return jsonify(403)
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        return jsonify(403)
    else:
        user.confirmed = True
        db.session.commit()
    return jsonify(200)


@auth_api.route('/api/resend/token', methods=['POST'])
def resend_confirm_token():
    if current_user.is_authenticated:
        if not current_user.confirmed:
            user = User.query.filter_by(
                username=current_user.username).first_or_404()
            token = generate_confirmation_token(user.email)
            send_email(to=user.email, subject='test', template=token)
    else:
        return jsonify(404)


@auth_api.route('/api/password/forget', methods=['POST'])
def forget_password_controller():
    email = request.json['email']
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify(403)
    token = generate_confirmation_token(email)
    return jsonify(token)


@auth_api.route('/api/password/r<token>', methods=['POST'])
def reset_password_controller(token):
    newPassword = request.json['password']
    try:
        email = confirm_token(token)
    except BaseException:
        return jsonify(403)

    user = User.query.filter_by(email=email).first_or_404()
    user.password = bcrypt.generate_password_hash(newPassword)
    db.session.commit()
    return jsonify(200)