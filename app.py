from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load the model
model = joblib.load("webapp/api/models/svc.save")
scaler = joblib.load("webapp/api/models/scaler.save")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        features = [float(x) for x in request.form.values()]
        scaled_features = scaler.transform([features])
        prediction = model.predict(scaled_features)
        result = "Potable" if prediction[0] == 1 else "Not Potable"
        return render_template("prediction.html", prediction_text=f"Water is {result}")
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
