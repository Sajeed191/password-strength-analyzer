from flask import Flask, render_template, request, redirect, session, jsonify
import random
import string

app = Flask(__name__)
app.secret_key = "secret123"

# Dummy user database
users = {
    "admin": "admin123"
}

# Password strength function
def password_strength(password):

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


# LOGIN
@app.route("/", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:

            session["user"] = username
            return redirect("/dashboard")

    return render_template("login.html")


# DASHBOARD
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    return render_template("dashboard.html", user=session["user"])


# PASSWORD STRENGTH
@app.route("/strength", methods=["GET","POST"])
def strength():

    result = None
    score = None

    if request.method == "POST":

        password = request.form["password"]

        score = password_strength(password)

        if score <= 25:
            result = "POOR"

        elif score <= 50:
            result = "WEAK"

        elif score <= 75:
            result = "GOOD"

        else:
            result = "EXCELLENT"

    return render_template("strength.html", result=result, score=score)


# PASSWORD GENERATOR
@app.route("/generate_password")
def generate_password():

    characters = string.ascii_letters + string.digits + "!@#$%^&*"

    password = "".join(random.choice(characters) for i in range(12))

    return jsonify({"password": password})


# LOGOUT
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
