from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import random
import string

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY","secret")

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/database.db"

app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ---------------- DATABASE ---------------- #

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(150), unique=True)

    email = db.Column(db.String(150))

    password = db.Column(db.String(200))

    profile_image = db.Column(db.String(200), default="default.png")


class Analytics(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)

    strength = db.Column(db.String(50))


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()

# ---------------- PASSWORD ANALYZER ---------------- #

def analyze_password(password):

    score = 0

    if len(password) >= 8:
        score += 25

    if any(c.isupper() for c in password):
        score += 25

    if any(c.isdigit() for c in password):
        score += 25

    if any(c in "!@#$%^&*" for c in password):
        score += 25

    if score <= 25:
        strength = "Weak"
    elif score <= 75:
        strength = "Medium"
    else:
        strength = "Strong"

    return score, strength


# ---------------- PASSWORD SUGGESTION ---------------- #

def generate_password():

    letters = string.ascii_letters
    digits = string.digits
    symbols = "!@#$%^&*"

    password = "".join(random.choice(letters+digits+symbols) for i in range(12))

    return password


# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    return redirect(url_for("login"))


# REGISTER

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        user = User(username=username,email=email,password=password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


# LOGIN

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password,password):

            login_user(user)

            return redirect(url_for("dashboard"))

    return render_template("login.html")


# DASHBOARD

@app.route("/dashboard", methods=["GET","POST"])
@login_required
def dashboard():

    strength = ""
    percentage = 0

    if request.method == "POST":

        password = request.form["password"]

        percentage, strength = analyze_password(password)

        data = Analytics(user_id=current_user.id,strength=strength)

        db.session.add(data)
        db.session.commit()

    strong = Analytics.query.filter_by(user_id=current_user.id,strength="Strong").count()
    medium = Analytics.query.filter_by(user_id=current_user.id,strength="Medium").count()
    weak = Analytics.query.filter_by(user_id=current_user.id,strength="Weak").count()

    suggestion = generate_password()

    return render_template(
        "dashboard.html",
        strength=strength,
        percentage=percentage,
        strong=strong,
        medium=medium,
        weak=weak,
        suggestion=suggestion
    )


# PROFILE IMAGE UPLOAD

@app.route("/profile", methods=["GET","POST"])
@login_required
def profile():

    if request.method == "POST":

        file = request.files["image"]

        filename = secure_filename(file.filename)

        path = os.path.join(app.config["UPLOAD_FOLDER"],filename)

        file.save(path)

        current_user.profile_image = filename

        db.session.commit()

    return render_template("profile.html")


# LOGOUT

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))


if __name__ == "__main__":

    port = int(os.environ.get("PORT",5000))

    app.run(host="0.0.0.0",port=port)
