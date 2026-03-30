import joblib

model = joblib.load('heatwave_model.pkl')

MODEL_VERSION = 1.0.0

def predict_heatwave(user_input: dict):
    input_df = pd.DataFrame(user_input)

    output_prediction = model.predict(features)[0]           # 0 or 1
    output_probability = model.predict_proba(features)[0][1]

    return output_prediction, output_probability