from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Secret key for sessions
app.config['SECRET_KEY'] = 'secret123'

# SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# -----------------------------
# Database Model
# -----------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


# -----------------------------
# Home Route
# -----------------------------
@app.route('/')
def home():
    return redirect(url_for('login'))


# -----------------------------
# Register
# -----------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        # Check if username exists
        user = User.query.filter_by(username=username).first()

        if user:
            flash("Username already exists. Please choose another.", "danger")
            return redirect(url_for('register'))

        # Hash password
        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            password=hashed_password
        )

        try:
            db.session.add(new_user)
            db.session.commit()

            flash("Account created successfully!", "success")
            return redirect(url_for('login'))

        except Exception as e:
            db.session.rollback()
            flash("Registration failed. Try again.", "danger")
            return redirect(url_for('register'))

    return render_template('register.html')


# -----------------------------
# Login
# -----------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            session['user_id'] = user.id
            session['username'] = user.username

            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))

        else:
            flash("Invalid username or password.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')


# -----------------------------
# Dashboard
# -----------------------------
@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html')


# -----------------------------
# Logout
# -----------------------------
@app.route('/logout')
def logout():

    session.clear()
    flash("Logged out successfully.", "info")

    return redirect(url_for('login'))


# -----------------------------
# Create Database
# -----------------------------
with app.app_context():
    db.create_all()


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
