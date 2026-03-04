from flask import Flask, render_template, request, jsonify, redirect, session
import re
import hashlib
import requests
import sqlite3
import random
import string
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "super_secure_secret_key"

# -------------------------
# DATABASE SETUP
# -------------------------
def init_db():
    conn = sqlite3.connect("analytics.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT,
            strength INTEGER,
            level TEXT,
            breach_count INTEGER,
            similarity INTEGER,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -------------------------
# PASSWORD STRENGTH ENGINE
# -------------------------
def check_strength(password):
    score = 0
    if len(password) >= 8: score += 20
    if re.search("[A-Z]", password): score += 20
    if re.search("[a-z]", password): score += 20
    if re.search("[0-9]", password): score += 20
    if re.search("[@#$%^&*!]", password): score += 20
    return score

def get_level(score):
    if score < 40:
        return "Poor"
    elif score < 60:
        return "Weak"
    elif score < 80:
        return "Good"
    else:
        return "Excellent"

# -------------------------
# BREACH CHECK
# -------------------------
def check_breach(password):
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    if response.status_code != 200:
        return 0

    hashes = (line.split(":") for line in response.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return int(count)
    return 0

# -------------------------
# PASSWORD SUGGESTION
# -------------------------
def suggest_password(password):
    extra = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return password + "@" + extra

# -------------------------
# SAVE ANALYTICS
# -------------------------
def save_data(website, strength, level, breach_count, similarity):
    conn = sqlite3.connect("analytics.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO analytics (website, strength, level, breach_count, similarity, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (website, strength, level, breach_count, similarity,
          datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

# -------------------------
# ROUTES
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check():
    data = request.json
    password = data.get("password")
    website = data.get("website")

    strength = check_strength(password)
    level = get_level(strength)
    breach_count = check_breach(password)

    # Simulated similarity percentage
    similarity = random.randint(5, 75)

    suggestion = suggest_password(password)

    save_data(website, strength, level, breach_count, similarity)

    return jsonify({
        "strength": strength,
        "level": level,
        "breach_count": breach_count,
        "similarity": similarity,
        "suggestion": suggestion
    })

# -------------------------
# ADMIN LOGIN
# -------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin123":
            session["admin"] = True
            return redirect("/dashboard")
        return "Invalid Credentials"

    return render_template("login.html")

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
    <h2>CyberShield Admin Dashboard</h2>
    <p>Total Checks: {total}</p>
    <p>Weak Passwords: {weak}</p>
    <p>Breached Passwords: {breached}</p>
    <br><a href='/logout'>Logout</a>
    """

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/login")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
