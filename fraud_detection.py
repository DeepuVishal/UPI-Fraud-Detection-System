import pandas as pd
import pickle


def detect_fraud(input_data):
    """
    Takes a dictionary of input and returns the fraud probability.
    """
    with open('fraud_model.pkl', 'rb') as f:
        assets = pickle.load(f)

    # Prepare the dataframe for prediction
    df_input = pd.DataFrame([input_data])

    # Encode categorical values using the saved encoders
    for col in assets['encoders']:
        if col in df_input.columns:
            le = assets['encoders'][col]
            # Handle unseen categories gracefully
            df_input[col] = df_input[col].apply(lambda x: le.transform([str(x)])[0] if str(x) in le.classes_ else -1)

    # Reorder columns to match the training features
    X_input = df_input[assets['features']]

    # Get probability of fraud (class 1)
    prob = assets['model'].predict_proba(X_input)[0][1]
    prediction = assets['model'].predict(X_input)[0]

    return prediction, prob