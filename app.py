from flask import Flask, render_template, request
import main  # we will modify main.py to accept inputs

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run():
    skills = [s.strip() for s in request.form["skills"].split(",") if s.strip()]
    experience = int(request.form["experience"])
    education = request.form["education"]

    # Call your ATS logic (we'll modify main.py for this)
    results = main.run_screening(skills, experience, education)

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)