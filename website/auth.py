from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user,
)  # Session - stores logged in user
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)  # hash the password

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            # removelater
            print("Returned data from login request:", user, type(user), user.email)
            if check_password_hash(
                user.password, password
            ):  # compares object returned from database and hash the second
                flash("Logged in", category="success")
                login_user(user, remember=True)  # store user object to session variable
                return redirect(url_for("views.home"))  # rerouting to homepage
            else:
                flash("Password is incorrect.", category="error")
        else:
            flash("Email does not exist.", category="error")
            
    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required  # can only access the logout function if currently logged in(Session data exist)
def logout():
    logout_user()  # removes data stored from session
    return redirect(url_for("views.home"))  # rerouting to homepage


@auth.route("/signup", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        # removelater
        print("Returned from sign up request:", email_exists, type(email_exists))
        username_exists = User.query.filter_by(username=username).first()
        # removelater
        print("Returned from sign up request:", username_exists, type(username_exists))

        if email_exists:
            flash("Email already exist.", category="error")
        elif username_exists:
            flash("Username already exists.", category="error")
        elif password1 != password2:
            flash("Password don't match!", category="error")
        elif len(username) < 2:
            flash("Username is too short.", category="error")
        elif len(password1) < 3:
            flash("Password is too short.", category="error")
        elif len(email) < 4:
            flash("Email is too short.", category="error")
        else:
            # removelater
            print("Password hash:", generate_password_hash(password1, method="sha256"))
            new_user = User(
                email=email,
                username=username,
                password=generate_password_hash(password1, method="sha256"),
            )
            db.session.add(new_user)  # staging
            db.session.commit()  # puts in the database
            login_user(new_user, remember=True)  # stores website session data
            flash("User created!")
            return redirect(url_for("views.home"))

    return render_template("signup.html", user=current_user)
