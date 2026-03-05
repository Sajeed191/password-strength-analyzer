import os

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# ---------------- CONFIG ---------------- #

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "devsecret")

# Detect production database (Render PostgreSQL)
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
else:
    # Local fallback database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# ---------------- DATABASE MODELS ---------------- #

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(150), unique=True, nullable=False)

    email = db.Column(db.String(150), nullable=False)

    password = db.Column(db.String(200), nullable=False)


# ---------------- USER LOADER ---------------- #

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------------- CREATE TABLES ---------------- #

with app.app_context():
    db.create_all()


# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    return redirect(url_for("login"))


# REGISTER

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        try:

            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]

            hashed_password = generate_password_hash(password)

            existing_user = User.query.filter_by(username=username).first()

            if existing_user:
                return "Username already exists"

            new_user = User(
                username=username,
                email=email,
                password=hashed_password
            )

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for("login"))

        except Exception as e:
            return f"Register error: {str(e)}"

    return render_template("register.html")


# LOGIN

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            return redirect(url_for("dashboard"))

        return "Invalid username or password"

    return render_template("login.html")


# DASHBOARD

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template("dashboard.html")


# LOGOUT

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))


# ---------------- RUN SERVER ---------------- #

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)
