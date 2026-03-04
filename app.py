from flask import Flask, render_template, request, jsonify, redirect, url_for
import re
import math
import random
import string
import os

app = Flask(__name__)

history = []
common_passwords = ["123456", "password", "qwerty", "admin", "welcome"]

# -------------------------
# PASSWORD LOGIC
# -------------------------

def calculate_strength(password):
    score = 0

    if len(password) >= 8: score += 15
    if len(password) >= 12: score += 10
    if re.search("[A-Z]", password): score += 15
    if re.search("[a-z]", password): score += 15
    if re.search("[0-9]", password): score += 15
    if re.search("[^A-Za-z0-9]", password): score += 20

    if password.lower() in common_passwords:
        score -= 30

    if re.search(r"(1234|abcd|qwer)", password.lower()):
        score -= 15

    return max(min(score, 100), 0)

def entropy(password):
    pool = 0
    if re.search("[a-z]", password): pool += 26
    if re.search("[A-Z]", password): pool += 26
    if re.search("[0-9]", password): pool += 10
    if re.search("[^A-Za-z0-9]", password): pool += 32
    if pool == 0:
        return 0
    return round(len(password) * math.log2(pool), 2)

def risk_level(score):
    if score < 30: return "Critical Risk"
    elif score < 50: return "High Risk"
    elif score < 75: return "Medium Risk"
    elif score < 90: return "Low Risk"
    else: return "Very Secure"

def similarity_simulation():
    sites = ["Amazon", "Flipkart", "Ajio", "Instagram", "Gmail"]
    return {site: random.randint(5, 40) for site in sites}

def generate_password(length):
    chars = string.ascii_letters + string.digits + "@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

# -------------------------
# ROUTES
# -------------------------

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    password = data.get("password", "")

    score = calculate_strength(password)
    ent = entropy(password)
    risk = risk_level(score)
    similarity = similarity_simulation()

    history.append(password)
    last_history = history[-5:]

    return jsonify({
        "strength": score,
        "entropy": ent,
        "risk": risk,
        "similarity": similarity,
        "history": last_history
    })

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    length = int(data.get("length", 12))
    new_password = generate_password(length)
    return jsonify({"password": new_password})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
