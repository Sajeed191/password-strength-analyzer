from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# SECRET KEY
app.config['SECRET_KEY'] = 'secret123'

# DATABASE PATH
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "instance", "user.db")

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


# ======================
# DATABASE MODEL
# ======================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# ======================
# ROUTES
# ======================

@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return render_template("index.html")


# ======================
# REGISTER
# ======================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("User already exists")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration Successful")
        return redirect(url_for("login"))

    return render_template("register.html")


# ======================
# LOGIN
# ======================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))

        flash("Invalid Login")

    return render_template("login.html")


# ======================
# DASHBOARD
# ======================

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


# ======================
# PROFILE
# ======================

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


# ======================
# PASSWORD CHECK
# ======================

@app.route("/result", methods=["POST"])
@login_required
def result():

    password = request.form.get("password")

    score = 0

    if len(password) >= 8:
        score += 1
    if any(char.isdigit() for char in password):
        score += 1
    if any(char.isupper() for char in password):
        score += 1
    if any(char in "!@#$%^&*" for char in password):
        score += 1

    if score <= 1:
        strength = "Weak"
    elif score == 2:
        strength = "Medium"
    else:
        strength = "Strong"

    return render_template("result.html", strength=strength)


# ======================
# ADMIN PAGE
# ======================

@app.route("/admin")
@login_required
def admin():

    users = User.query.all()

    return render_template("admin.html", users=users)


# ======================
# LOGOUT
# ======================

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# ======================
# RUN APP
# ======================

if __name__ == "__main__":

    os.makedirs("instance", exist_ok=True)

    with app.app_context():
        db.create_all()

    app.run(debug=True)
