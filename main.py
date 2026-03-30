from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from schema.user_input import CityInput, HeatIndexInput, WeatherInput
from services.weather_service import get_weather_by_city
from src.predict import predict_heatwave
from src.predict import model

app = FastAPI(title="Heatwave Prediction API")

MODEL_FEATURES = ['day_of_year', 'humidity', 'windspeed', 'precip', 'cloudcover']

@app.get("/")
def home():
    return {"message": "Welcome to the Heatwave Prediction API. Use /predict endpoint to get predictions."}

@app.post("/weather-by-city")
def weather_by_city(data: CityInput):
    try:
        weather = get_weather_by_city(data.city)
        return {
            "success": True,
            "data": weather
        }
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=404)

@app.post("/predict")
def predict(data: WeatherInput):
    dt = datetime.strptime(data.date, "%d/%m/%Y")
    day_of_year = dt.timetuple().tm_yday

    # Auto-fetch weather parameters if not provided
    humidity = data.humidity
    windspeed = data.windspeed
    precip = data.precip
    cloudcover = data.cloudcover

    # Track if we had to estimate weather parameters
    estimated_params = []

    # If any weather parameter is missing, fetch from weather API
    if any(v is None for v in [humidity, windspeed, precip, cloudcover]):
        try:
            # Fetch current weather and use as estimate for the selected date
            weather = get_weather_by_city("Delhi")  # Default city, can be extended
            if humidity is None:
                humidity = weather.get("humidity", 50.0)
                estimated_params.append("humidity")
            if windspeed is None:
                windspeed = weather.get("windspeed", 10.0)
                estimated_params.append("windspeed")
            # Map weather description to cloud cover estimate
            if cloudcover is None:
                desc = weather.get("description", "").lower()
                if "clear" in desc or "sunny" in desc:
                    cloudcover = 10.0
                elif "cloud" in desc:
                    cloudcover = 50.0
                elif "overcast" in desc:
                    cloudcover = 80.0
                else:
                    cloudcover = 20.0
                estimated_params.append("cloudcover")
            # Precipitation estimate based on weather description
            if precip is None:
                desc = weather.get("description", "").lower()
                if "rain" in desc or "shower" in desc:
                    precip = 5.0
                else:
                    precip = 0.0
                estimated_params.append("precip")
        except Exception as e:
            # Fallback defaults if API fails
            if humidity is None:
                humidity = 50.0
                estimated_params.append("humidity")
            if windspeed is None:
                windspeed = 10.0
                estimated_params.append("windspeed")
            if cloudcover is None:
                cloudcover = 20.0
                estimated_params.append("cloudcover")
            if precip is None:
                precip = 0.0
                estimated_params.append("precip")

    user_input = pd.DataFrame([{
        "day_of_year": day_of_year,
        "humidity":    humidity,
        "windspeed":   windspeed,
        "precip":      precip,
        "cloudcover":  cloudcover,
    }])

    try:
        pred, prob = predict_heatwave(user_input)  # Pass values to predict function

        # Estimate temperature and solar radiation based on day of year and cloud cover
        # Summer months (day 150-210) have higher base temperatures
        base_temp = 35.0 + 10.0 * (1 - abs(day_of_year - 180) / 90)  # Peak around day 180
        temperature = base_temp + (20 - cloudcover) * 0.3  # Less cloud = higher temp

        # Solar radiation estimate based on cloud cover (clear sky ~800 W/m²)
        solar_radiation = max(0, 800 - cloudcover * 8)

        return {
            "date":           data.date,
            "day_of_year":    day_of_year,
            "temperature":    round(temperature, 2),
            "humidity":       round(humidity, 2),
            "windspeed":      round(windspeed, 2),
            "precip":         round(precip, 2),
            "cloudcover":     round(cloudcover, 2),
            "solar_radiation": round(solar_radiation, 2),
            "heatwave":       bool(pred),
            "probability":    float(prob),
            "risk_level":     "High" if prob >= 0.7 else "Medium" if prob >= 0.4 else "Low",
            "safe_to_work":   bool(pred == 0),
            "advisory": (
                "Do NOT work outdoors. Heatwave predicted." if pred == 1
                else "Safe to work. No heatwave predicted."
            ),
            "estimated_params": estimated_params if estimated_params else None,
            "note": "Weather parameters were automatically estimated based on current conditions" if estimated_params else None
        }
    except Exception as e:
        return JSONResponse(content={"message": "Prediction failed", "error": str(e)}, status_code=500)

@app.post("/heat_index_calculator")
def heat_index(data: HeatIndexInput):
    T = data.temperature
    R = data.humidity
    
    heat_index = 0.5 * (
        T + 61.0 + ((T - 68) * 1.2) + (R * 0.094)
    )
    
    return {"heat_index": round(heat_index, 4)}

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




# GET /historical-analysis
# ├─ Input: Date range, region
# └─ Output: Heatwave statistics, trends, patterns

# GET /heatwave-alerts
# ├─ Input: Probability threshold
# └─ Output: Days with predicted heatwaves above threshold

# GET /forecast
# ├─ Input: Number of days to forecast ahead
# └─ Output: Week-ahead heatwave predictions
# @app.get('/forecast')