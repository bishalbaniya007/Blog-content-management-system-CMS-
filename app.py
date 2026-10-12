from dotenv import load_dotenv
import os
from flask import Flask
from flask_wtf import CSRFProtect

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

csrf = CSRFProtect(app)

from routes.admin import admin
from routes.auth import auth
from routes.main import main
from routes.posts import posts
 
app.register_blueprint(admin)
app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(posts)

if __name__ == "__main__":
  app.run(debug=True)



