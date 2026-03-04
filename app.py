import os
import re
import random
import string
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# =========================
# App Configuration
# =========================

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "fallback_secret_key")

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    "DATABASE_URL", "sqlite:///securevault.db"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# =========================
# Database Model
# =========================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# =========================
# Password Strength Logic
# =========================

def check_password_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"\d", password):
        score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1

    percentage = (score / 5) * 100

    if percentage <= 40:
        strength = "Poor"
    elif percentage <= 60:
        strength = "Weak"
    elif percentage <= 80:
        strength = "Good"
    else:
        strength = "Excellent"

    return percentage, strength

# =========================
# Password Generator
# =========================

def generate_strong_password(base_password):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_part = ''.join(random.choice(characters) for _ in range(6))
    return base_password + random_part

# =========================
# Routes
# =========================

@app.route("/")
def home():
    return render_template("index.html")

# -------- Register --------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        hashed_password = generate_password_hash(password)

        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# -------- Login --------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials", "danger")

    return render_template("login.html")

# -------- Dashboard --------

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    percentage = None
    strength = None
    generated_password = None

    if request.method == "POST":
        password = request.form.get("password")

        percentage, strength = check_password_strength(password)
        generated_password = generate_strong_password(password)

    return render_template(
        "dashboard.html",
        percentage=percentage,
        strength=strength,
        generated_password=generated_password
    )

# -------- Logout --------

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))

# =========================
# Create Database
# =========================

with app.app_context():
    db.create_all()

# =========================
# Run App (Render Compatible)
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
