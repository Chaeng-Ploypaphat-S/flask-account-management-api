from flask import Flask
from .routes import main as main_blueprint
from .models import db
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'mysecretkey'
    app.config['JWT_SECRET_KEY'] = 'myjwtsecretkey'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 86400

    jwt = JWTManager(app)

    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.init_app(app)
        db.create_all()
        
    jwt.init_app(app)
    
    return app