from flask import Blueprint, jsonify, request
from flask_login import LoginManager, login_user, login_required
from .models import User, db

main = Blueprint('main', __name__)
login_manager = LoginManager()

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
    user = User(username=data['username'], email=data['email'], password_hash=data['password'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'id': user.id}), 201


@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or any(
        key not in data for key in ('username', 'email', 'password')
    ):
        return jsonify({'error': 'Missing data'}), 400

    if User.query.filter_by(username=data['username']).first() is not None:
        return jsonify({'error': 'Username already exists'}), 400

    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'Registration successful'}), 201

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or any(key not in data for key in ('username', 'password')):
        return jsonify({'error': 'Missing data'}), 400

    user = User.query.filter_by(username=data['username']).first()
    if user is None or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401

    login_user(user)

    return jsonify({'message': 'Login successful'}), 200

@main.route('/protected', methods=['GET'])
@login_required
def protected():
    return jsonify({'message': 'This is a protected route'}), 200