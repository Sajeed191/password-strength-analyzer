from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secretkey123"

# Dummy user database
users = {
    "admin": "1234",
    "sajeed": "password"
}

@app.route('/')
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route('/login', methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)


@app.route('/dashboard')
def dashboard():
    if "user" in session:
        return f"""
        <h2>Welcome {session['user']}!</h2>
        <a href='/logout'>Logout</a>
        """
    return redirect(url_for("login"))


@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
