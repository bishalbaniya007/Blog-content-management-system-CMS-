# APPLICATION FACTORY PATTERN

from flask import Flask
from config import Config
from app.extensions import db, migrate, login_manager, csrf

def create_app(config_class = Config):
  app = Flask(__name__)

  app.config.from_object(config_class)

  db.init_app(app) # Initializes Flask-SQLAlchemy with your application.

  migrate.init_app(app, db) # Connects Flask-Migrate to the Flask application and the SQLAlchemy database extension.
  # The app argument tells it which Flask application to work with.
  # The db argument tells it which database metadata and models to use for migration operations.

  login_manager.init_app(app) # Initializes Flask-Login for your application.
  # It allows Flask-Login to manage login-related behavior.

  csrf.init_app(app)

  from app.routes.main import main
  from app.routes.auth import auth
  from app.routes.admin import admin
  from app.routes.posts import posts

  app.register_blueprint(main)
  app.register_blueprint(auth)
  app.register_blueprint(admin)
  app.register_blueprint(posts)

  return app



