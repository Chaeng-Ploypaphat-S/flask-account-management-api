import unittest
from flask import Flask
from app.routes import main
from app.models import db, User

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(self.app)
        self.app.register_blueprint(main)
        with self.app.app_context():
            db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_users_empty(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_create_user(self):
        data = {'username': 'testuser', 'email': 'test@example.com'}
        response = self.client.post('/user', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.get_json())

    def test_get_users_after_create(self):
        # Create a user
        data = {'username': 'John Smith', 'email': 'user@test.com'}
        self.client.post('/user', json=data)
        # Get users
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        users = response.get_json()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]['username'], 'John Smith')
        self.assertEqual(users[0]['email'], 'user@test.com')

if __name__ == '__main__':
    unittest.main()