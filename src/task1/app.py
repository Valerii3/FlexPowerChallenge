from flask import Flask
from src.task1.config import DevelopmentConfig
from src.task1.extensions import db, ma
from src.task1.routes import trade_bp


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(trade_bp, url_prefix='/v1')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)