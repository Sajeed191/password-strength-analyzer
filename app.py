from flask import Flask, render_template, request, jsonify
import re
import random
import string

app = Flask(__name__)

# Check password strength score
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

# Generate strong suggestion
def generate_suggestion(password):
    extra = ''.join(random.choices(string.ascii_letters + string.digits + "@#$%", k=5))
    return password.capitalize() + extra

# Simulate similar password usage %
def similar_usage(password, website):
    common_patterns = ["123", "password", "admin", website.lower()]
    match_score = sum(pattern in password.lower() for pattern in common_patterns)
    return min(90, match_score * 25 + random.randint(5, 20))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check():
    data = request.json
    password = data.get("password", "")
    website = data.get("website", "")

    strength = check_strength(password)
    suggestion = generate_suggestion(password)
    similarity = similar_usage(password, website)

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
        "suggestion": suggestion,
        "similarity": similarity
    })

if __name__ == "__main__":
    app.run(debug=True)
