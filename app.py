from flask import Flask, request, jsonify
import pandas as pd
import joblib
import re

app = Flask(__name__)

# Load the trained model
model = joblib.load("phishing_model.pkl")

# Feature extraction function
def extract_features(url):
    if not isinstance(url, str):
        return [0, 0, 0, 0, 0]

    return [
        len(url),
        sum(c.isdigit() for c in url),
        len(re.findall(r"[\W_]", url)),  # Special characters
        url.count("."),
        1 if url.startswith("https") else 0
    ]

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = ['url_length', 'has_ip', 'contains_at_symbol', 'has_https', 'domain_age']  # <-- match your model features

    input_df = pd.DataFrame([data], columns=features)  # wrap in a list to create 1 row

    prediction = model.predict(input_df)[0]

    result = {
        "is_phishing": bool(prediction),
        "url": data.get("url", "N/A")
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # Use port 10000 for Render
