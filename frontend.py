import streamlit as st
import requests

st.set_page_config(
    page_title="Indian Flight Price Predictor",
    page_icon="✈️",
    layout="centered"
)

BACKEND_URL = "http://127.0.0.1:8000/predict"

st.title("✈️ Indian Flight Price Prediction")
st.write(
    "Select flight itinerary and booking details to get the predicted ticket fare in INR (₹)."
)

with st.form("flight_prediction_form"):
    st.subheader("📋 Flight Details")

    col1, col2 = st.columns(2)

    with col1:
        airline = st.selectbox(
            "Airline",
            options=["Vistara", "Air_India", "Indigo", "GO_FIRST", "AirAsia", "SpiceJet"],
            index=0
        )

        source_city = st.selectbox(
            "Source City",
            options=["Delhi", "Mumbai", "Bangalore", "Kolkata", "Hyderabad", "Chennai"],
            index=0
        )

        departure_time = st.selectbox(
            "Departure Time",
            options=["Early_Morning", "Morning", "Afternoon", "Evening", "Night", "Late_Night"],
            index=1
        )

        flight_class = st.selectbox(
            "Class",
            options=["Economy", "Business"],
            index=0
        )

    with col2:
        destination_city = st.selectbox(
            "Destination City",
            options=["Mumbai", "Delhi", "Bangalore", "Kolkata", "Hyderabad", "Chennai"],
            index=0
        )

        arrival_time = st.selectbox(
            "Arrival Time",
            options=["Early_Morning", "Morning", "Afternoon", "Evening", "Night", "Late_Night"],
            index=3
        )

        stops = st.selectbox(
            "Number of Stops",
            options=["zero", "one", "two_or_more"],
            index=0
        )

    st.subheader("⏱️ Flight Timing & Booking Window")
    
    duration = st.slider(
        "Flight Duration (in hours)",
        min_value=0.5,
        max_value=50.0,
        value=2.25,
        step=0.25
    )

    days_left = st.slider(
        "Days Left for Departure",
        min_value=1,
        max_value=50,
        value=15,
        step=1
    )

    submit_button = st.form_submit_button("🔮 Predict Flight Fare")

if submit_button:
    if source_city == destination_city:
        st.warning("⚠️ Source City aur Destination City alag hone chahiye!")
    else:
        payload = {
            "airline": airline,
            "source_city": source_city,
            "departure_time": departure_time,
            "stops": stops,
            "arrival_time": arrival_time,
            "destination_city": destination_city,
            "class": flight_class,
            "duration": float(duration),
            "days_left": int(days_left)
        }

        with st.spinner("Fetching prediction from backend..."):
            try:
                response = requests.post(
                    BACKEND_URL,
                    json=payload,
                    timeout=30
                )

                if response.ok:
                    result = response.json()

                    if result.get("status") == "success":
                        fare = result.get("predicted_price_inr")
                        st.success(f"🎉 Estimated Flight Price: ₹{fare:,.2f}")
                    else:
                        st.error(f"Unexpected response from backend: {result}")
                else:
                    st.error(f"Backend returned HTTP {response.status_code}")
                    st.code(response.text)

            except requests.exceptions.ConnectionError:
                st.error(
                    "❌ FastAPI backend se connect nahi ho paya. "
                    "Make sure karein ki backend terminal par `uvicorn app:app --reload` port 8000 pe chal raha hai."
                )

            except requests.exceptions.Timeout:
                st.error("⏳ Backend request timed out.")

            except requests.exceptions.RequestException as exc:
                st.error(f"Request failed: {exc}")

            except ValueError:
                st.error("Invalid response format received from backend.")