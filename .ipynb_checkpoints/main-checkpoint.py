# import pandas as pd
# from datetime import datetime
# from pydantic import BaseModel, field_validator

# class Weather(BaseModel):
#     probability_threshold: Annotated[float]
#     days: Field(...,gt=0,description='prediction of next days')
#     solar_radiation: Annotated[float]
#     Wind_speed: Annotated[float, Field(..., description='wind should be in km/h',example='35.5')]
#     humidity: Annotated[float, Field(...,description='humidity should be int',example='51.2')]
#     temp: Annotated[float, Field(..., gt=20,lt=60,description='temperature should be in degree celsius',example='39*C')]
#     date: str
#     @field_validator("date")
#     def validate_date(cls, v):
#         try:
#             datetime.strptime(v, "%d/%m/%Y")
#         except ValueError:
#             raise ValueError("Date must be in dd/mm/yyyy format")
#         return v

# @app.get('/forecast')
# def forcast():

# @app.get('/heatwave_alert')
# def heatwave_alert():


# GET /historical-analysis
# ├─ Input: Date range, region
# └─ Output: Heatwave statistics, trends, patterns

# GET /heatwave-alerts
# ├─ Input: Probability threshold
# └─ Output: Days with predicted heatwaves above threshold


from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from schema.user_input import WeatherInput
from src.predict import predict_heatwave
from src.predict import model

app = FastAPI(title="Heatwave Prediction API")

MODEL_FEATURES = ['day_of_year', 'humidity', 'windspeed', 'precip', 'cloudcover']

@app.get("/")
def home():
    return {"message": "Welcome to the Heatwave Prediction API. Use /predict endpoint to get predictions."}

@app.post("/predict")
def predict(data: WeatherInput):
    dt = datetime.strptime(data.date, "%d/%m/%Y")
    day_of_year = dt.timetuple().tm_yday

    user_input = pd.DataFrame([{
        "day_of_year": day_of_year,
        "humidity":    data.humidity,
        "windspeed":   data.windspeed,
        "precip":      data.precip,
        "cloudcover":  data.cloudcover,
    }])

    try:
        pred, prob = predict_heatwave(user_input)  # Pass values to predict function
        return {
            "date":         data.date,
            "day_of_year":  day_of_year,
            "heatwave":     bool(pred),
            "probability":  float(prob),
            "risk_level":   "High" if prob >= 0.7 else "Medium" if prob >= 0.4 else "Low",
            "safe_to_work": bool(pred == 0),
            "advisory": (
                "Do NOT work outdoors. Heatwave predicted." if pred == 1
                else "Safe to work. No heatwave predicted."
            )
        }  
    except Exception as e:
        return JSONResponse(content={"message": "Prediction failed", "error": str(e)}, status_code=500)

# GET /forecast
# ├─ Input: Number of days to forecast ahead
# └─ Output: Week-ahead heatwave predictions



# GET /heat-index-calculator
# ├─ Input: temperature, humidity
# └─ Output: Calculated heat index value

# @app.get('/heat_index_calculator')
# def heat_index_calculator():


# GET /model-health
# ├─ Output: Model performance metrics, last training date, accuracy

@app.get("/model-health")
def model_health():
    return {
        "status":         "healthy",
        "model_type":     str(type(model).__name__),
        "input_features": MODEL_FEATURES,
        "output":         "0 = No Heatwave, 1 = Heatwave",
        "model_version":  "1.0.0",
        "last_trained":   "2024-06-01",
        "accuracy":       "92.5%"
    }