from flask import Flask, request, jsonify
import joblib
import re

app = Flask(__name__)

# Load the trained model
model = joblib.load("/Users/yashvardhansinghsolanki/Desktop/Github/PhishGuard/ml_model/phishing_model.pkl")

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

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    
    if "url" not in data:
        return jsonify({"error": "No URL provided"}), 400

    url = data["url"]
    features = extract_features(url)
    
    # Predict using the model
    prediction = model.predict([features])[0]
    
    return jsonify({"url": url, "is_phishing": bool(prediction)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # Use port 10000 for Render
