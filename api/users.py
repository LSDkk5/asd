from flask_restful import Resource
from flask import Blueprint, request, jsonify, abort

from web.models import User
from web import api

api_users = Blueprint('api_users', __name__)

def abort_if_user_doesnt_exist(username):
    if not User.query.filter_by(username=username):
        abort(404, message="User {} doesn't exist".format(username))

class ApiUserList(Resource):
    def get(self):
        users = User.query.all()
        return str(users)
    
    def post(self):
        registerData = {
            'username': request.json['username'],
            'password': request.json['password'],
            'rpassword': request.json['rpassword'],
            'email': request.json['email']}
        print(registerData)

class ApiUser(Resource):
    def get(self, username):
        return str(User.query.filter_by(username=username).first_or_404())

api.add_resource(ApiUserList, '/api/v1.0/user')
api.add_resource(ApiUser, '/api/v1.0/user/<username>')
