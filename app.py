from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

def check_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if re.search("[A-Z]", password):
        score += 1
    if re.search("[a-z]", password):
        score += 1
    if re.search("[0-9]", password):
        score += 1
    if re.search("[@#$%^&*!]", password):
        score += 1

    if score <= 2:
        return "Weak"
    elif score == 3 or score == 4:
        return "Medium"
    else:
        return "Strong"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check():
    password = request.json["password"]
    result = check_strength(password)
    with open("history.txt", "a") as file:
    file.write(f"{password} - {result}\n")

return jsonify({"strength": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)