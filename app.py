import random
import string

@app.route("/strength", methods=["GET","POST"])
def strength():

    result = None
    percent = None
    suggestions = []

    if request.method == "POST":

        password = request.form["password"]
        website = request.form["website"]

        score = security_score(password)

        # strength label
        if score <= 25:
            result = "POOR"
        elif score <= 50:
            result = "WEAK"
        elif score <= 75:
            result = "GOOD"
        else:
            result = "EXCELLENT"

        # simulated similarity percentages
        site_stats = {
            "amazon": random.randint(10,40),
            "flipkart": random.randint(20,50),
            "ajio": random.randint(15,45),
            "myntra": random.randint(10,35)
        }

        percent = site_stats.get(website.lower(), random.randint(10,50))

        # generate stronger suggestions
        for i in range(3):

            strong = password + random.choice(string.punctuation) + str(random.randint(10,99))
            suggestions.append(strong)

    return render_template(
        "strength.html",
        result=result,
        percent=percent,
        suggestions=suggestions
    )
