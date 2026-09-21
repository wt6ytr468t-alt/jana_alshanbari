from flask import Flask, render_template, request

app = Flask(__name__)

# Concentration in mg/mL. 
CONCENTRATIONS = {
    "120": 24,   # 120 mg / 5 mL
    "125": 25,   # 125 mg / 5 mL
    "160": 32,   # 160 mg / 5 mL
    "100": 100,  # 100 mg / 1 mL
}

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None

    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            age = int(request.form.get("age", 0))
            weight = float(request.form.get("weight", 0))
            strength = request.form.get("strength", "")

            if not name:
                raise ValueError("Please enter the patient's name.")
            if not 1 <= age <= 144:
                raise ValueError("This prototype supports ages 3–144 months only.")
            if not 0 < weight <= 150:
                raise ValueError("Enter a valid weight in kg.")
            if strength not in CONCENTRATIONS:
                raise ValueError("Please select a valid concentration.")

            concentration = CONCENTRATIONS[strength]

            # DEMONSTRATION FORMULA ONLY — NOT A CLINICAL DOSING RULE.
            dose_mg = weight * 10
            dose_ml = dose_mg / concentration

            result = {
                "name": name, "age": age, "weight": weight,
                "dose_mg": round(dose_mg, 1),
                "dose_ml": round(dose_ml, 2),
            }
        except (ValueError, TypeError) as exc:
            error = str(exc) or "Invalid information. Please check your entries."

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)
