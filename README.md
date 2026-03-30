# 🌡️ Heatwave Prediction API

**Production-Ready Heatwave Forecasting System**

A full end-to-end machine learning system that predicts heatwave conditions and assesses outdoor work safety — built with industry-standard MLOps practices including model serving, real-time weather integration, and Docker deployment.

---

## 📋 Table of Contents

- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Model Overview](#-model-overview)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Extending the Project](#-extending-the-project)

---

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────────────────────────────────────────┐
│   Client     │────▶│              FastAPI Service                     │
│  (curl/app)  │◀────│                                                  │
└─────────────┘     │  ┌──────────┐  ┌───────────┐  ┌──────────────┐  │
                    │  │  Pydantic │  │  Feature   │  │   Trained    │  │
                    │  │  Validate │─▶│  Builder   │─▶│   Model      │  │
                    │  └──────────┘  └───────────┘  └──────┬───────┘  │
                    │                                       │          │
                    │  ┌──────────────┐                     │          │
                    │  │  OpenWeather │◀────────────────────┘          │
                    │  │  API Client  │  (Auto-fetch missing params)   │
                    │  └──────────────┘                                 │
                    │                                                   │
                    │  ┌──────────────┐  ┌────────────────┐            │
                    │  │  Heat Index  │  │ Risk Advisory  │            │
                    │  │  Calculator  │  │ Generator       │            │
                    │  └──────────────┘  └────────────────┘            │
                    └──────────────────────────────────────────────────┘
```

### Prediction Flow

1. **Client** sends weather data via `POST /predict`
2. **Pydantic** validates the input schema (date, humidity, windspeed, etc.)
3. **Auto-Fetch** retrieves missing weather parameters from OpenWeather API
4. **Feature Builder** constructs the feature vector (day_of_year, humidity, windspeed, precip, cloudcover)
5. **Trained Model** returns heatwave probability
6. **Risk Advisory** generates safety recommendations and work advisories
7. **API** returns probability, risk level, and safety guidance

---

## 📁 Project Structure

```
summer-heat-wave/
│
├── main.py                     # FastAPI service & endpoints
├── schema/
│   └── user_input.py           # Pydantic request/response models
│
├── src/
│   ├── predict.py              # Model loading & prediction
│   └── Model.ipynb             # Model training notebook
│
├── services/
│   ├── weather_service.py      # OpenWeather API integration
│   └── api_service.py          # Additional API helpers
│
├── model/
│   └── heatwave_model.pkl      # Trained model artifact
│
├── data/
│   ├── raw/                    # Raw datasets
│   └── processed/              # Processed features
│
├── notebooks/                  # EDA & experimentation
│
├── frontend/                   # Frontend application (UI)
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── Dockerfile                  # Backend container definition
├── .dockerignore               # Docker ignore rules
├── requirements.txt            # Python dependencies
└── README.md
```
---

## 🖥️ Frontend

The project includes a frontend UI to interact with the Heatwave Prediction API.

### Features
- Submit weather input for prediction
- View heatwave risk level (`Low`, `Medium`, `High`)
- Display advisory and work-safety recommendation
- Fetch weather by city and prefill prediction inputs
- Heat Index calculator integration

---
---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- pip

### 1. Install Dependencies

```bash
cd summer-heat-wave
pip install -r requirements.txt
```

### 2. Start the API

```bash
uvicorn main:app --reload
```

### 3. Access the API

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive Swagger UI.

### 4. Make a Prediction

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "date": "15/06/2026",
    "humidity": 45.0,
    "windspeed": 12.5,
    "precip": 0.0,
    "cloudcover": 15.0
  }'
```

**Example Response:**

```json
{
  "date": "15/06/2026",
  "day_of_year": 166,
  "temperature": 42.35,
  "humidity": 45.0,
  "windspeed": 12.5,
  "precip": 0.0,
  "cloudcover": 15.0,
  "solar_radiation": 680.0,
  "heatwave": true,
  "probability": 0.87,
  "risk_level": "High",
  "safe_to_work": false,
  "advisory": "Do NOT work outdoors. Heatwave predicted.",
  "estimated_params": null,
  "note": null
}
```

### 5. Get Weather by City

```bash
curl -X POST http://localhost:8000/weather-by-city \
  -H "Content-Type: application/json" \
  -d '{"city": "Delhi"}'
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "city": "Delhi",
    "country": "IN",
    "temperature": 38.5,
    "humidity": 42,
    "windspeed": 14.2,
    "feels_like": 41.3,
    "description": "clear sky"
  }
}
```

### 6. Calculate Heat Index

```bash
curl -X POST http://localhost:8000/heat_index_calculator \
  -H "Content-Type: application/json" \
  -d '{"temperature": 35.0, "humidity": 60.0}'
```

**Example Response:**

```json
{
  "heat_index": 45.25
}
```

---

## 🧪 Model Overview

### Model Architecture

| Component | Description |
|-----------|-------------|
| **Model Type** | Scikit-learn Classifier |
| **Version** | 1.0.0 |
| **Accuracy** | 92.5% |
| **Last Trained** | 2024-06-01 |

### Input Features

| Feature | Description | Range |
|---------|-------------|-------|
| `day_of_year` | Day number (1-365) | 1-365 |
| `humidity` | Relative humidity | 0-100% |
| `windspeed` | Wind speed | 0-50 km/h |
| `precip` | Precipitation | 0-100 mm |
| `cloudcover` | Cloud coverage | 0-100% |

### Output

| Output | Description |
|--------|-------------|
| `heatwave` | Binary prediction (0 = No, 1 = Yes) |
| `probability` | Confidence score (0-1) |
| `risk_level` | Low / Medium / High |
| `safe_to_work` | Boolean work safety flag |

### Risk Levels

| Probability | Risk Level | Advisory |
|-------------|------------|----------|
| >= 0.7 | **High** | Do NOT work outdoors |
| 0.4 - 0.7 | **Medium** | Exercise caution |
| < 0.4 | **Low** | Safe to work |

---

## 📡 API Documentation

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check & welcome message |
| `/predict` | POST | Predict heatwave for given weather |
| `/weather-by-city` | POST | Fetch real-time weather data |
| `/heat_index_calculator` | POST | Calculate heat index from temp & humidity |
| `/model-health` | GET | Model metadata & status |

### Request Schemas

#### `WeatherInput` (POST /predict)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `date` | string | Yes | dd/mm/yyyy format |
| `humidity` | float | No | Percentage (auto-fetched if missing) |
| `windspeed` | float | No | km/h (auto-fetched if missing) |
| `precip` | float | No | mm (auto-fetched if missing) |
| `cloudcover` | float | No | Percentage (auto-fetched if missing) |

#### `CityInput` (POST /weather-by-city)

| Field | Type | Description |
|-------|------|-------------|
| `city` | string | City name (e.g., "Jaipur", "Delhi") |

#### `HeatIndexInput` (POST /heat_index_calculator)

| Field | Type | Description |
|-------|------|-------------|
| `temperature` | float | Temperature in Celsius |
| `humidity` | float | Relative humidity percentage |

### Response Schemas

#### `GET /model-health`

```json
{
  "status": "healthy",
  "model_type": "RandomForestClassifier",
  "input_features": ["day_of_year", "humidity", "windspeed", "precip", "cloudcover"],
  "output": "0 = No Heatwave, 1 = Heatwave",
  "model_version": "1.0.0",
  "last_trained": "2024-06-01",
  "accuracy": "92.5%"
}
```

---

## 🐳 Deployment

### Docker

```bash
# Build
docker build -t heatwave-prediction-api .

# Run
docker run -p 8000:8000 heatwave-prediction-api
```

### Local Development

```bash
uvicorn main:app --reload --port 8000
```

---

## 🔮 Extending the Project

| Enhancement | Description |
|-------------|-------------|
| **Historical Analysis** | Add `/historical-analysis` endpoint for trend analysis |
| **Heatwave Alerts** | Add `/heatwave-alerts` for threshold-based notifications |
| **Week Forecast** | Add `/forecast` endpoint for 7-day ahead predictions |
| **Multi-City Support** | Extend `/predict` to accept city parameter |
| **MLflow Integration** | Track experiments and register model versions |
| **Grafana Dashboard** | Visualize prediction metrics and model health |
| **Automated Retraining** | Schedule periodic model retraining with new data |
| **SMS/Email Alerts** | Integrate Twilio/SendGrid for heatwave warnings |
| **Geospatial Mapping** | Add map-based visualization of heatwave risk |
| **Mobile App** | Build React Native/Flutter app for field workers |

---

## 📄 License

This project is intended for educational and portfolio purposes.

---

Built with ❤️ using FastAPI, scikit-learn, pandas, and Docker.
