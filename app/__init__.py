from flask import Flask
from .routes import main as main_blueprint
from .models import db, User
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'

login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(main_blueprint)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app():
    with app.app_context():
        db.init_app(app)
        db.create_all()
    return app