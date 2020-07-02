from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from project.configs import Config


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


def register_blueprints(app):
    from project.endpoints.users import blueprint as usuarios
    from project.endpoints.status import blueprint as status

    app.register_blueprint(usuarios)
    app.register_blueprint(status)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    register_blueprints(app)

    return app
