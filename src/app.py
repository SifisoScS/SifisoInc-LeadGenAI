import os
from flask import Flask, render_template, request, redirect, url_for
from crew import leadgen_crew
from leadgen import save_leads_to_csv, read_leads_from_csv

app = Flask(__name__)

# Ensure output folder exists
OUTPUT_FOLDER = "output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    leads = read_leads_from_csv()  # Load leads from CSV
    if request.method == "POST":
        industry = request.form["industry"]
        result = leadgen_crew.kickoff(inputs={"industry": industry})  # Run LeadGen AI
        save_leads_to_csv(result)  # Save results
        return redirect(url_for("index"))  # Refresh page
    return render_template("index.html", leads=leads)

if __name__ == "__main__":
    app.run(debug=True)  # Start Flask app
