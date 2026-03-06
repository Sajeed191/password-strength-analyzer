from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import math
import re
import random
import string
import hashlib
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret123"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# =====================
# DATABASE MODEL
# =====================

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True)

    password = db.Column(db.String(200))


# =====================
# LOGIN MANAGER
# =====================

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# =====================
# PASSWORD STRENGTH
# =====================

def password_strength(password):

    score = 0

    if len(password) >= 8:
        score += 1

    if re.search("[A-Z]", password):
        score += 1

    if re.search("[0-9]", password):
        score += 1

    if re.search("[@#$%^&*!]", password):
        score += 1

    if score <= 1:
        return "Weak"

    elif score == 2:
        return "Medium"

    elif score == 3:
        return "Strong"

    else:
        return "Very Strong"


# =====================
# PASSWORD ENTROPY
# =====================

def entropy(password):

    charset = 0

    if re.search("[a-z]", password):
        charset += 26

    if re.search("[A-Z]", password):
        charset += 26

    if re.search("[0-9]", password):
        charset += 10

    if re.search("[@#$%^&*!]", password):
        charset += 32

    if charset == 0:
        return 0

    return round(len(password) * math.log2(charset), 2)


# =====================
# PASSWORD GENERATOR
# =====================

def generate_password():

    chars = string.ascii_letters + string.digits + "@#$%^&*!?"

    password = ''.join(random.choice(chars) for _ in range(14))

    return password


# =====================
# DATA BREACH CHECK
# =====================

def check_breach(password):

    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()

    prefix = sha1[:5]

    suffix = sha1[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    res = requests.get(url)

    hashes = (line.split(":") for line in res.text.splitlines())

    for h, count in hashes:

        if h == suffix:
            return True

    return False


# =====================
# HOME
# =====================

@app.route("/")
@login_required
def home():

    return render_template("index.html")


# =====================
# ANALYZE PASSWORD
# =====================

@app.route("/analyze", methods=["POST"])
@login_required
def analyze():

    password = request.form.get("password")

    strength = password_strength(password)

    ent = entropy(password)

    breach = check_breach(password)

    return render_template(
        "result.html",
        strength=strength,
        entropy=ent,
        breach=breach
    )


# =====================
# PASSWORD GENERATOR
# =====================

@app.route("/generate")
@login_required
def generate():

    pwd = generate_password()

    return jsonify({"password": pwd})


# =====================
# DASHBOARD
# =====================

@app.route("/dashboard")
@login_required
def dashboard():

    data = {
        "weak": 4,
        "medium": 6,
        "strong": 3
    }

    return render_template("dashboard.html", data=data)


# =====================
# REGISTER
# =====================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        hashed = generate_password_hash(password)

        user = User(username=username, password=hashed)

        db.session.add(user)

        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


# =====================
# LOGIN
# =====================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            return redirect(url_for("home"))

    return render_template("login.html")


# =====================
# LOGOUT
# =====================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))


# =====================
# START APP
# =====================

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)
