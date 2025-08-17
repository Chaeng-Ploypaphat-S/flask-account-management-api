from flask import Blueprint, jsonify, request
from .models import User, db

main = Blueprint('main', __name__)

@main.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([
        {'username': user.username, 'email': user.email}
        for user in users
    ])


@main.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(username=data['username'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id}), 201