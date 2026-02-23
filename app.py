from flask import Flask, render_template, request
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

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        password = request.form["password"]
        result = check_strength(password)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
