from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import requests
import streamlit as st
from services.api_service import HeatwaveService

# service = HeatwaveService("http://43.205.140.153")
# API_URL = "http://43.205.140.153"  
service = HeatwaveService("http://localhost")
API_URL = "http://localhost"  
st.title("🌡️ Heatwave System")

option = st.radio(
    "Choose what you want to do:",
    ["Predict Heatwave", "Calculate Heat Index", "Get Weather by City"])


# -------------------------
# 🔥 Predict
# -------------------------
if option == "Predict Heatwave":
    st.header("🔥 Heatwave Prediction")

    date = st.date_input("Select date", key="date")

    if st.button("Predict"):
        data = {
            "date": date.strftime("%d/%m/%Y")
        }

        result, error = service.predict_heatwave(data)

        if error:
            st.error(error)
        else:
            st.success("Prediction completed")

            # Weather Parameters Section
            st.subheader("🌤️ Weather Parameters")
            col1, col2, col3 = st.columns(3)
            col1.metric("Temperature", f"{result.get('temperature', 'N/A')}°C")
            col2.metric("Humidity", f"{result.get('humidity', 'N/A')}%")
            col3.metric("Wind Speed", f"{result.get('windspeed', 'N/A')} km/h")

            col4, col5, col6 = st.columns(3)
            col4.metric("Precipitation", f"{result.get('precip', 'N/A')} mm")
            col5.metric("Cloud Cover", f"{result.get('cloudcover', 'N/A')}%")
            col6.metric("Solar Radiation", f"{result.get('solar_radiation', 'N/A')} W/m²")

            st.divider()

            # Heatwave Prediction Section
            st.subheader("🔥 Heatwave Prediction")
            c1, c2, c3 = st.columns(3)
            c1.metric("Heatwave", "Yes" if result.get("heatwave") else "No")
            c2.metric("Probability", f"{result.get('probability', 0) * 100:.2f}%")
            c3.metric("Risk Level", result.get("risk_level", "N/A"))

            st.write(f"**Date:** {result.get('date', 'N/A')}")
            st.write(f"**Day of Year:** {result.get('day_of_year', 'N/A')}")
            st.write(f"**Safe to Work:** {'Yes' if result.get('safe_to_work') else 'No'}")
            st.info(result.get("advisory", "No advisory available"))

            if result.get("note"):
                st.warning(result.get("note"))


# -------------------------
# 🌡️ Heat Index
# -------------------------
elif option == "Calculate Heat Index":
    st.header("🌡️ Heat Index Calculator")

    temperature = st.number_input("Temperature", key="temp_hi")
    humidity = st.number_input("Humidity", key="hum_hi")

    if st.button("Calculate"):
        data = {
            "temperature": temperature,
            "humidity": humidity
        }

        result, error = service.calculate_heat_index(data)

        if error:
            st.error(error)
        else:
            heat_index_value = result.get("heat_index") if isinstance(result, dict) else result
            st.success(f"Heat Index: {heat_index_value}")

# -------------------------
# 🌆 Weather by City
elif option == "Get Weather by City":
    st.header("🌍 Get Weather by City")

    city = st.text_input("Enter city name:", "Delhi")

    if st.button("🔍 Fetch Weather"):
        response = requests.post(f"{API_URL}/weather-by-city", json={"city": city})

        if response.status_code == 200:
            result = response.json()
            weather = result["data"]
            st.success(f"Weather in {weather['city']}, {weather['country']}")
            st.write(f"🌡️ Temperature: {weather['temperature']}°C")
            st.write(f"💧 Humidity: {weather['humidity']}%")
            st.write(f"💨 Wind Speed: {weather['windspeed']} km/h")
            st.write(f"📝 feels_like: {weather['feels_like']}°C")
            st.write(f"📝 Description: {weather['description'].title()}")
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
