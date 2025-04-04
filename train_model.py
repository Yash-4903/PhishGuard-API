import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load processed data
df = pd.read_csv("processed_data.csv")

# Define input features and labels
X = df.drop(columns=["URL"])  # Drop URL column
y = [1] * len(df)  # Assume all are phishing (we need more balanced data later)

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model trained with accuracy: {accuracy:.2f}")

# Save the trained model
joblib.dump(model, "phishing_model.pkl")
print("✅ Model saved as phishing_model.pkl")
