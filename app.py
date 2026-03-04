from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import os, random, string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# ---------------- DATABASE ----------------

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))
    profile_image = db.Column(db.String(200), default="default.png")

class Analytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    strength = db.Column(db.String(50))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --------------- PASSWORD LOGIC -------------

def analyze_password(password):
    score = 0
    if len(password) >= 8: score += 25
    if any(c.isupper() for c in password): score += 25
    if any(c.isdigit() for c in password): score += 25
    if any(c in "!@#$%^&*" for c in password): score += 25

    if score <= 25:
        strength = "Weak"
    elif score <= 75:
        strength = "Medium"
    else:
        strength = "Strong"

    return score, strength

# --------------- ROUTES ---------------------

@app.route("/dashboard", methods=["GET","POST"])
@login_required
def dashboard():
    percentage = 0
    strength = ""

    if request.method == "POST":
        password = request.form["password"]
        percentage, strength = analyze_password(password)

        new_data = Analytics(user_id=current_user.id, strength=strength)
        db.session.add(new_data)
        db.session.commit()

    total = Analytics.query.filter_by(user_id=current_user.id).count()
    strong = Analytics.query.filter_by(user_id=current_user.id, strength="Strong").count()
    weak = Analytics.query.filter_by(user_id=current_user.id, strength="Weak").count()

    return render_template("dashboard.html",
                           percentage=percentage,
                           strength=strength,
                           total=total,
                           strong=strong,
                           weak=weak)

@app.route("/update_profile", methods=["POST"])
@login_required
def update_profile():
    current_user.username = request.form["username"]
    current_user.email = request.form["email"]

    if "profile_image" in request.files:
        file = request.files["profile_image"]
        if file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            current_user.profile_image = filename

    db.session.commit()
    return redirect(url_for("dashboard"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
