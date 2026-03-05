from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re
import os

app = Flask(__name__)

app.secret_key = "supersecretkey"

# DATABASE CONFIG (Render PostgreSQL)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


# -----------------------------
# User Model
# -----------------------------

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -----------------------------
# Password Strength Function
# -----------------------------

def check_password_strength(password):

    score = 0

    if len(password) >= 8:
        score += 1

    if re.search("[a-z]", password):
        score += 1

    if re.search("[A-Z]", password):
        score += 1

    if re.search("[0-9]", password):
        score += 1

    if re.search("[@#$%^&+=!]", password):
        score += 1

    if score <= 2:
        return "Weak"

    elif score == 3 or score == 4:
        return "Medium"

    else:
        return "Strong"


# -----------------------------
# Home
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Register
# -----------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please login.")

        return redirect(url_for("login"))

    return render_template("register.html")


# -----------------------------
# Login
# -----------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            return redirect(url_for("dashboard"))

        else:
            flash("Invalid login credentials")

    return render_template("login.html")


# -----------------------------
# Dashboard
# -----------------------------

@app.route("/dashboard")
@login_required
def dashboard():

    users = User.query.all()

    total_users = User.query.count()

    return render_template(
        "dashboard.html",
        users=users,
        total_users=total_users
    )


# -----------------------------
# Password Strength Checker
# -----------------------------

@app.route("/check_password", methods=["POST"])
@login_required
def check_password():

    password = request.form["password"]

    strength = check_password_strength(password)

    return render_template(
        "result.html",
        password=password,
        strength=strength
    )


# -----------------------------
# Logout
# -----------------------------

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))


# -----------------------------
# Run App
# -----------------------------

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)
