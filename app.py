from flask import Flask, render_template, request, jsonify
import re
import random
import string
import hashlib
import requests

app = Flask(__name__)

# Simple analytics counter
total_checks = 0
weak_passwords = 0

# -----------------------
# PASSWORD STRENGTH CHECK
# -----------------------
def check_strength(password):
    score = 0

    if len(password) >= 8:
        score += 20
    if re.search("[A-Z]", password):
        score += 20
    if re.search("[a-z]", password):
        score += 20
    if re.search("[0-9]", password):
        score += 20
    if re.search("[@#$%^&*!]", password):
        score += 20

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
# AI PASSWORD GENERATOR
# -----------------------
def generate_ultra_password():
    chars = string.ascii_letters + string.digits + "@#$%^&*!"
    return ''.join(random.choices(chars, k=16))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check():
    global total_checks, weak_passwords

    total_checks += 1

    data = request.json
    password = data.get("password", "")

    strength = check_strength(password)
    breach_count = check_breach(password)

    if strength < 60:
        weak_passwords += 1

    if strength < 40:
        level = "Poor"
    elif strength < 60:
        level = "Weak"
    elif strength < 80:
        level = "Good"
    else:
        level = "Excellent"

    return jsonify({
        "strength": strength,
        "level": level,
        "breach_count": breach_count,
        "total_checks": total_checks,
        "weak_passwords": weak_passwords
    })


@app.route("/generate", methods=["GET"])
def generate():
    return jsonify({
        "password": generate_ultra_password()
    })


if __name__ == "__main__":
    app.run(debug=True)
