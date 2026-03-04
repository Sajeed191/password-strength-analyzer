from flask import Flask, render_template, request, jsonify, redirect, session
import re
import hashlib
import requests
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey123"   # Change later for production

# -----------------------
# DATABASE SETUP
# -----------------------
def init_db():
    conn = sqlite3.connect("analytics.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            strength INTEGER,
            level TEXT,
            breach_count INTEGER,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# -----------------------
# PASSWORD STRENGTH
# -----------------------
def check_strength(password):
    score = 0
    if len(password) >= 8: score += 20
    if re.search("[A-Z]", password): score += 20
    if re.search("[a-z]", password): score += 20
    if re.search("[0-9]", password): score += 20
    if re.search("[@#$%^&*!]", password): score += 20
    return score

# -----------------------
# BREACH CHECK
# -----------------------
def check_breach(password):
    sha1_password = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1_password[:5]
    suffix = sha1_password[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    if response.status_code != 200:
        return 0

    hashes = (line.split(":") for line in response.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return int(count)
    return 0

# -----------------------
# SAVE ANALYTICS
# -----------------------
def save_to_db(strength, level, breach_count):
    conn = sqlite3.connect("analytics.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO analytics (strength, level, breach_count, timestamp) VALUES (?, ?, ?, ?)",
        (strength, level, breach_count, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

# -----------------------
# ROUTES
# -----------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check():
    data = request.json
    password = data.get("password", "")

    strength = check_strength(password)
    breach_count = check_breach(password)

    if strength < 40:
        level = "Poor"
    elif strength < 60:
        level = "Weak"
    elif strength < 80:
        level = "Good"
    else:
        level = "Excellent"

    save_to_db(strength, level, breach_count)

    return jsonify({
        "strength": strength,
        "level": level,
        "breach_count": breach_count
    })

# -----------------------
# ADMIN LOGIN
# -----------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # CHANGE THESE CREDENTIALS
        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect("/dashboard")
        else:
            return "Invalid credentials"

    return """
    <h2>Admin Login</h2>
    <form method="POST">
        <input name="username" placeholder="Username"><br><br>
        <input name="password" type="password" placeholder="Password"><br><br>
        <button type="submit">Login</button>
    </form>
    """

@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect("/login")

    conn = sqlite3.connect("analytics.db")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM analytics")
    total = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM analytics WHERE level='Weak' OR level='Poor'")
    weak = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM analytics WHERE breach_count > 0")
    breached = c.fetchone()[0]

    conn.close()

    return f"""
    <h2>Admin Dashboard</h2>
    <p>Total Checks: {total}</p>
    <p>Weak Passwords: {weak}</p>
    <p>Breached Passwords: {breached}</p>
    <br>
    <a href="/logout">Logout</a>
    """

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
