import unittest
from app.models import User, db
from app import create_app

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_user_creation(self):
        user = User(username='testuser', email='user_1@test.com')
        db.session.add(user)
        db.session.commit()
        self.assertIsNotNone(user.id)