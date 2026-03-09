import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
import pickle

# 1. Load dataset
df = pd.read_csv(r"C:\Users\DEEPIKA\PycharmProjects\upi_fraud_detection\dataset\fraud_data.csv")

# 2. Setup Encoders
upi_apps = ["Amazon Pay", "BHIM", "GPay", "Paytm", "PhonePe", "PayZapp", "WhatsApp Pay"]
banks = ["Axis", "BOB", "Canara", "HDFC", "ICICI", "Kotak", "PNB", "SBI"]
methods = ["QR Scan", "Mobile Number", "UPI ID"]

upi_encoder = LabelEncoder().fit(upi_apps)
bank_encoder = LabelEncoder().fit(banks)
payment_encoder = LabelEncoder().fit(methods)

df['UPI_App'] = upi_encoder.transform(df['UPI_App'])
df['Bank'] = bank_encoder.transform(df['Bank'])
df['Payment_Method'] = payment_encoder.transform(df['Payment_Method'])

# 3. Inputs & Target
X = df[['Amount', 'UPI_App', 'Bank', 'Payment_Method', 'Hour', 'Is_Night', 'Is_Weekend', 'Attempt_Count']]

# IMPORTANT: Ensure target is 0 and 1 (Integer)
y = df['is_suspicious'].astype(int)

# 4. Train XGBoost

model = xgb.XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,        # Reduced depth to prevent over-reacting
    scale_pos_weight=1,  # CHANGE THIS TO 1 (Balanced)
    eval_metric='logloss'
)

model.fit(X, y)

# 5. Save Everything
with open("train_model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("upi_encoder.pkl", "wb") as f:
    pickle.dump(upi_encoder, f)
with open("bank_encoder.pkl", "wb") as f:
    pickle.dump(bank_encoder, f)
with open("payment_encoder.pkl", "wb") as f:
    pickle.dump(payment_encoder, f)

print("✅ XGBoost Model trained and saved without warnings!")
