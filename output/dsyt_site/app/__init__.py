from __future__ import annotations

from pathlib import Path

import json
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth"


def create_app() -> Flask:
    app = Flask(__name__)
    root = Path(__file__).resolve().parents[1]
    config_path = root / "app_config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))

    app.config["SECRET_KEY"] = "dev-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dsyt.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["APP_CONFIG"] = config

    db.init_app(app)
    login_manager.init_app(app)

    from .models import User
    from .routes import register_routes
    from .seed import seed_market

    @login_manager.user_loader
    def load_user(user_id: str):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()
        seed_market(config)

    register_routes(app)
    return app
