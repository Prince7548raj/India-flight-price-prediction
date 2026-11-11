# ✈️ Indian Flight Price Prediction System

# Indian Flight Price Prediction System

The Indian Flight Price Prediction System is an end-to-end machine learning web application engineered to estimate domestic airfare fares across primary routes within India. Addressing complex market dynamics, booking intervals, seasonal trends, and route competition, the system delivers real-time airfare predictions derived from operational parameters such as carrier name, itinerary departure and arrival windows, intermediate stops, and ticket travel classes.
The end-to-end architecture integrates data preprocessing, regression modeling, and a decoupled service design. The backend service is built using FastAPI and served via Uvicorn to handle asynchronous REST API inference calls, querying an optimized machine learning pipeline constructed with Scikit-learn, XGBoost, Pandas, and NumPy. On the client side, a responsive Streamlit web interface provides an intuitive portal for parameter entry and dynamic prediction rendering.
The entire multi-tier stack is containerized using Docker and orchestrated via a unified entrypoint script managing both backend and frontend processes. The production container is hosted on an AWS EC2 instance running Ubuntu 26.04 LTS, configured with custom inbound network security rules allowing dedicated traffic on ports 8000 and 8501. The application ensures persistent deployment with automated recovery policies and supports seamless integration between client requests, API endpoints, and production machine learning models.

---

## 📌 Project Overview

Predicting airfare in India is challenging due to dynamic pricing, seasonal demand, route competition, and booking lead times. This application takes flight parameters (airline, departure/arrival schedules, stops, and travel class) and provides real-time ticket price predictions powered by an optimized machine learning model.

---

## 🛠️ Tech Stack & Architecture

- **Machine Learning & Data Processing:** Python 3.11, Scikit-learn, XGBoost, Pandas, NumPy, Joblib
- **Backend API:** FastAPI, Uvicorn
- **Frontend UI:** Streamlit
- **Containerization:** Docker (Multi-service deployment orchestrated via entrypoint)
- **Cloud Infrastructure:** AWS EC2 (Ubuntu 26.04 LTS)

---

## 🏛️ System Architecture

```text
       User Request
            │
            ▼
┌───────────────────────┐
│   Streamlit Frontend  │  (Port 8501)
└───────────┬───────────┘
            │  REST API Calls
            ▼
┌───────────────────────┐
│    FastAPI Backend    │  (Port 8000)
└───────────┬───────────┘
            │  Inference
            ▼
┌───────────────────────┐
│   Trained ML Model    │  (my_model.pkl)
└───────────────────────┘
