from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import re
import math

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkey123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# ================= DATABASE =================

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# ================= PASSWORD STRENGTH =================

def check_password_strength(password):

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


# ================= PASSWORD ENTROPY =================

def password_entropy(password):

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

    entropy = len(password) * math.log2(charset)

    return round(entropy, 2)


# ================= HOME =================

@app.route("/")
@login_required
def home():

    return render_template("index.html")


# ================= ANALYZE PASSWORD =================

@app.route("/analyze", methods=["POST"])
@login_required
def analyze():

    password = request.form.get("password")

    strength = check_password_strength(password)

    entropy = password_entropy(password)

    return render_template(
        "result.html",
        strength=strength,
        entropy=entropy
    )


# ================= DASHBOARD =================

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template("dashboard.html")


# ================= REGISTER =================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user:
            flash("Username already exists")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful")

        return redirect(url_for("login"))

    return render_template("register.html")


# ================= LOGIN =================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            return redirect(url_for("home"))

        else:

            flash("Invalid username or password")

    return render_template("login.html")


# ================= LOGOUT =================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))


# ================= RUN =================

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)
