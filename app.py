from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "secret123"

# temporary user storage (replace with database later)
users = {}

@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


# REGISTER
@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username in users:
            flash("Username already exists!")
            return redirect(url_for("register"))

        users[username] = password

        flash("Account created successfully!")
        return redirect(url_for("login"))

    return render_template("register.html")


# LOGIN
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("dashboard"))

        flash("Invalid username or password")

    return render_template("login.html")


# DASHBOARD
@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        weak=4,
        medium=6,
        strong=3
    )


# LOGOUT
@app.route("/logout")
def logout():

    session.pop("username", None)
    flash("Logged out successfully")

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
