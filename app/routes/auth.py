from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select
from app.extensions import db
from app.models import User
from app.forms.auth_form import RegistrationForm, LoginForm

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["GET", "POST"])
def register():
  form = RegistrationForm()

  # validate on submit only return true if vlaid data and method == POST
  if form.validate_on_submit():
    # creating a user instance with the data submitted through forms
    user = User(
      username = form.username.data,
      email = form.email.data.lower(),
      password_hash = generate_password_hash(form.password.data)
    )

    db.session.add(user)
    db.session.commit()
    flash("Account created successfully.")

    return(redirect(url_for("auth.login")))

  return render_template("register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
  form = LoginForm()

  if form.validate_on_submit():
    # checking if user exists through email and fetching one if it does exist
    user = db.session.scalar(
      select(User).where(User.email == form.email.data.lower())
    )

    if user and check_password_hash(user.password_hash, form.password.data):
      login_user(user)
      flash("Logged in successfully.")
      return redirect(url_for("main.dashboard"))

    flash("Invalid email or password.")

  return render_template("login.html", form=form)


@auth.route("/logout", methods=["POST"])
@login_required
def logout():
  logout_user()
  flash("You have been logged out.")
  return redirect(url_for('auth.login'))

