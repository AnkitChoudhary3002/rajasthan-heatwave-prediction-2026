# 🔥 Heatwave Prediction in Rajasthan (Summer 2026)

## 📌 Project Overview
This project focuses on predicting **heatwave conditions in Rajasthan for Summer 2026** using historical daily climate data.  
The current implementation analyses summer-season heatwaves, while the underlying dataset contains multi-year daily meteorological records, enabling extension to daily forecasting and time-series modelling in a production environment.

The project is being developed as a **scalable machine learning pipeline**, with emphasis on maintainability, reproducibility, and future deployment.

---

## 🎯 Objectives
- Analyze historical temperature and humidity patterns related to heatwaves  
- Compute heat index and classify heatwave severity  
- Build a baseline predictive model for summer heatwaves  
- Design a pipeline that supports daily forecasting  
- Prepare the system for time-series forecasting and production use  

---

## 📊 Dataset
- Multi-year **daily climate data**  
- Features include:
  - Temperature  
  - Humidity  
  - Wind speed  
  - Solar radiation  
  - Derived heat index  
- Although the dataset covers **all seasons and years**, the current notebook focuses on **summer months** for problem scoping.

---

## 🧠 Methodology
- Data cleaning and preprocessing  
- Seasonal filtering for summer analysis  
- Feature engineering (heat index calculation)  
- Heatwave labelling using threshold-based criteria  
- Exploratory data analysis and visualization  
- Baseline machine learning model training and evaluation  

---
## 🔁 Pipeline Design (Production-Oriented)
The project is structured as an **end-to-end ML pipeline**:

- The same pipeline can operate on **daily incoming data**  
- Supports rolling evaluation and future automation  
- Designed to transition smoothly into **time-series forecasting models**

---

## 🚧 Current Status
- ✅ Data preprocessing and exploratory data analysis (EDA)  
- ✅ Heat index computation and heatwave classification  
- ✅ Baseline model development  
- 🚧 Modular pipeline implementation (in progress)  
- 🚧 Daily forecasting evaluation  
- 🚧 Model versioning and deployment  

---

## 🔮 Future Work
- Convert notebooks into modular Python scripts  
- Implement daily automated forecasting  
- Extend model to time-series approaches (ARIMA / ML with lag features / LSTM)  
- Add API or dashboard for real-time predictions  
- Introduce logging, monitoring, and model version control  

---

## 🛠️ Tech Stack
- Python  
- Pandas, NumPy  
- Matplotlib / Seaborn  
- Scikit-learn  
- Jupyter Notebook  

---

## 📌 Why This Project
This project is designed as a **production-ready climate analytics system**, suitable for continuous prediction, evaluation, and future deployment.
