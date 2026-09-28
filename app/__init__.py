from flask import Flask

from app.database import init_app as init_database


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    init_database(app)

    from app.routes import bp

    app.register_blueprint(bp)
    return app