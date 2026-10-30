from flask import Blueprint, render_template
from flask_login import login_user, logout_user, login_required

main = Blueprint("main", __name__)

@main.route("/")
def home():
  return render_template("base.html")


@main.route("/dashboard")
@login_required
def dashboard():
  return render_template("dashboard.html")