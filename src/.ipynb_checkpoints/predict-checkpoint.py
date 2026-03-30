import joblib
import pandas as pd

model = joblib.load('heatwave_model.pkl')

MODEL_VERSION = '1.0.0'

def predict_heatwave(user_input: pd.DataFrame):  # ✅ accepts DataFrame directly
    output_prediction = model.predict(user_input)[0]
    output_probability = model.predict_proba(user_input)[0][1]

    return output_prediction, output_probability