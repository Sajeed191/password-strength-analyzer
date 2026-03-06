from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp
import requests
import hashlib
import time

app = Flask(__name__)
app.secret_key = "supersecretkey"


# DATABASE CONNECTION
def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


# DATABASE TABLES
def init_db():

    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        otp_secret TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        action TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

init_db()


# PASSWORD BREACH CHECKER
def check_breach(password):

    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]

    url = "https://api.pwnedpasswords.com/range/" + prefix
    res = requests.get(url)

    hashes = (line.split(":") for line in res.text.splitlines())

    for h, count in hashes:
        if h == suffix:
            return int(count)

    return 0


# SECURITY SCORE
def security_score(password):

    score = 0

    if len(password) >= 8:
        score += 25

    if any(c.isupper() for c in password):
        score += 25

    if any(c.isdigit() for c in password):
        score += 25

    if any(c in "!@#$%^&*" for c in password):
        score += 25

    return score


# LOGIN ATTEMPT PROTECTION
failed_attempts = {}


# LOGIN
@app.route("/", methods=["GET","POST"])
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username in failed_attempts and failed_attempts[username] >= 3:
            flash("Too many attempts. Try later.")
            return redirect("/login")

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):

            session["tmp_user"] = username
            failed_attempts[username] = 0

            conn = get_db()
            conn.execute(
                "INSERT INTO logs(username,action) VALUES (?,?)",
                (username,"login success")
            )
            conn.commit()
            conn.close()

            return redirect("/verify")

        else:

            failed_attempts[username] = failed_attempts.get(username,0) + 1

            conn = get_db()
            conn.execute(
                "INSERT INTO logs(username,action) VALUES (?,?)",
                (username,"login failed")
            )
            conn.commit()
            conn.close()

            flash("Invalid login")

    return render_template("login.html")


# REGISTER
@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        breach = check_breach(password)

        if breach > 0:
            flash("Password found in data breaches!")

        hashed = generate_password_hash(password)

        otp_secret = pyotp.random_base32()

        conn = get_db()

        try:

            conn.execute(
                "INSERT INTO users(username,password,otp_secret) VALUES (?,?,?)",
                (username,hashed,otp_secret)
            )

            conn.commit()

            conn.execute(
                "INSERT INTO logs(username,action) VALUES (?,?)",
                (username,"account created")
            )

            conn.commit()

            flash("Account created")

            return redirect("/login")

        except:

            flash("Username already exists")

        conn.close()

    return render_template("register.html")


# OTP VERIFICATION
@app.route("/verify", methods=["GET","POST"])
def verify():

    if "tmp_user" not in session:
        return redirect("/login")

    if request.method == "POST":

        otp = request.form["otp"]

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (session["tmp_user"],)
        ).fetchone()

        conn.close()

        totp = pyotp.TOTP(user["otp_secret"])

        if totp.verify(otp):

            session["user"] = session["tmp_user"]
            session.pop("tmp_user")

            return redirect("/dashboard")

        else:

            flash("Invalid OTP")

    return render_template("verify_otp.html")


# DASHBOARD
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    conn = get_db()

    logs = conn.execute(
        "SELECT * FROM logs WHERE username=? ORDER BY timestamp DESC LIMIT 5",
        (session["user"],)
    ).fetchall()

    conn.close()

    score = 75

    return render_template(
        "dashboard.html",
        logs=logs,
        score=score
    )


# LOGOUT
@app.route("/logout")
def logout():

    conn = get_db()

    conn.execute(
        "INSERT INTO logs(username,action) VALUES (?,?)",
        (session["user"],"logout")
    )

    conn.commit()
    conn.close()

    session.clear()

    return redirect("/login")


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

