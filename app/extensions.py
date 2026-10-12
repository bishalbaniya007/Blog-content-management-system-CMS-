from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
# Connects your Flask application to SQLAlchemy's database and ORM functionality. 
# You use it with models and database sessions.


migrate = Migrate()
# Manages database schema migrations, usually through Alembic.
# For example, it helps apply changes when you add a column to a model.


login_manager = LoginManager()
# Manages user-login sessions, loading users, and checking whether a user is authenticated.


csrf = CSRFProtect()
# Helps protect against cross-site request forgery by validating CSRF tokens on applicable requests.