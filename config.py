# A file that holds your app's settings in one place, so they aren't scattered through the code.
import os
from dotenv import load_dotenv

load_dotenv()

# Its purpose is to group configuration settings together.
class Config():
  SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-key")    # dev-only-key -> defaul_value if no secret key
  SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///blog.db") # URI stands for Uniform Resource Identifier.

  SQLALCHEMY_TRACK_MODIFICATIONS = False # tracks changes to objects and emits signals when changes occur if set to True.


class TestConfig(Config):
  TESTING = True # This tells Flask that the application is running in testing mode.
  SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

  # This overrides the database URI inherited from Config.
  # In the normal configuration, your application uses the configured database URL or falls back to sqlite:///blog.db.
  # In the testing configuration, it instead uses an in-memory SQLite database.
