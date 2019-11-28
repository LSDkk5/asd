from flask_restful import Resource
from flask import Blueprint, request, jsonify, abort
import json

from web.models import User
from web import api

api_users = Blueprint('api_users', __name__)


class ApiUserList(Resource):
    def get(self):
        users = User.query.all()
        data = []

        for u in users:
            data.append({dict(
                user_id=u.id,
                username=u.username,
                email=u.email
            )})
        print(data)
        return jsonify(users=data)

class ApiUser(Resource):
    def get(self, username):
        user = User.query.filter_by(username=username).first_or_404()
        return jsonify(user=dict(user_id=user.id, username=user.username, email=user.email))

api.add_resource(ApiUserList, '/api/v1.0/users')
api.add_resource(ApiUser, '/api/v1.0/users/<username>')
