from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

import config

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    csrf.init_app(app)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    # 블루프린트
    from .views import main_views, user_views, board_views, board_article_views, dashboard_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(user_views.bp)
    app.register_blueprint(board_views.bp)
    app.register_blueprint(board_article_views.bp)
    app.register_blueprint(dashboard_views.bp)

    return app
