from flask import Flask, render_template, request, jsonify
import random
import re

app = Flask(__name__)

# Dummy similarity dataset (for project purpose)
website_similarity = {
    "Amazon": random.randint(10,60),
    "Flipkart": random.randint(10,60),
    "Ajio": random.randint(10,60),
    "Myntra": random.randint(10,60),
    "Instagram": random.randint(10,60)
}

def check_strength(password):

    score = 0

    if len(password) >= 8:
        score += 1

    if re.search("[a-z]", password):
        score += 1

    if re.search("[A-Z]", password):
        score += 1

    if re.search("[0-9]", password):
        score += 1

    if re.search("[@#$%^&*!]", password):
        score += 1

    levels = {
        1: "Poor",
        2: "Weak",
        3: "Medium",
        4: "Strong",
        5: "Excellent"
    }

    return levels.get(score, "Poor"), score*20


def suggest_password(password):

    suggestions = []

    for i in range(3):
        new = password + str(random.randint(10,99)) + "@"
        suggestions.append(new)

    return suggestions


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/analyze', methods=["POST"])
def analyze():

    data = request.json
    password = data["password"]
    website = data["website"]

    strength, percent = check_strength(password)

    similarity = website_similarity.get(website, random.randint(10,60))

    suggestions = suggest_password(password)

    return jsonify({
        "strength": strength,
        "percent": percent,
        "similarity": similarity,
        "suggestions": suggestions
    })


if __name__ == "__main__":
    app.run(debug=True)
