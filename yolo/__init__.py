from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    from .routes.analyze import analyze_bp
    from .routes.test_api import test_api_bp

    app.register_blueprint(analyze_bp)
    app.register_blueprint(test_api_bp)

    return app
