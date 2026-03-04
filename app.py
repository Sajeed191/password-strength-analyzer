from flask import Flask, render_template, request, jsonify
import re
import math
import random
import string
import hashlib
import requests
import os

app = Flask(__name__)

# -------------------------
# ADVANCED STRENGTH ENGINE
# -------------------------
def calculate_strength(password):
    score = 0
    length = len(password)

    if length >= 8: score += 20
    if length >= 12: score += 10
    if re.search("[A-Z]", password): score += 15
    if re.search("[a-z]", password): score += 15
    if re.search("[0-9]", password): score += 15
    if re.search("[^A-Za-z0-9]", password): score += 25

    return min(score, 100)

def entropy(password):
    pool = 0
    if re.search("[a-z]", password): pool += 26
    if re.search("[A-Z]", password): pool += 26
    if re.search("[0-9]", password): pool += 10
    if re.search("[^A-Za-z0-9]", password): pool += 32
    if pool == 0:
        return 0
    return round(len(password) * math.log2(pool), 2)

def suggest_improvement(password):
    if len(password) < 8:
        password += "Secure"
    if not re.search("[A-Z]", password):
        password += random.choice(string.ascii_uppercase)
    if not re.search("[0-9]", password):
        password += random.choice(string.digits)
    if not re.search("[^A-Za-z0-9]", password):
        password += random.choice("@#$%")
    return password

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    password = data.get("password", "")

    strength = calculate_strength(password)
    ent = entropy(password)
    suggestion = suggest_improvement(password)

    return jsonify({
        "strength": strength,
        "entropy": ent,
        "suggestion": suggestion
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
