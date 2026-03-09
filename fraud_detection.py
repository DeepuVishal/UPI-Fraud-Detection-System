import joblib
import pandas as pd

# Load trained model
model = joblib.load("fraud_model.pkl")


def predict_fraud(amount, hour_of_day, attempt_count, fraud_score,
                  is_night_transaction, is_weekend):
    # Create dataframe for prediction
    data = pd.DataFrame({
        "amount": [amount],
        "hour_of_day": [hour_of_day],
        "attempt_count": [attempt_count],
        "fraud_score": [fraud_score],
        "is_night_transaction": [is_night_transaction],
        "is_weekend": [is_weekend]
    })

    # Predict
    prediction = model.predict(data)

    if prediction[0] == 1:
        return "🚨 Fraudulent Transaction Detected"
    else:
        return "✅ Legitimate Transaction"
