from pathlib import Path
import pickle
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Indian Flight Price Prediction API")

# Model path resolve karna (same folder mein 'my_model.pkl' hona chahiye)
MODEL_PATH = Path(__file__).resolve().parent / "my_model.pkl"

with MODEL_PATH.open("rb") as file:
    loaded_model = pickle.load(file)


# Flight prediction ke exact feature schema ke hisaab se Pydantic model
class FlightInput(BaseModel):
    airline: str = Field(..., example="Vistara")
    source_city: str = Field(..., example="Delhi")
    departure_time: str = Field(..., example="Morning")
    stops: str = Field(..., example="zero")
    arrival_time: str = Field(..., example="Afternoon")
    destination_city: str = Field(..., example="Mumbai")
    flight_class: str = Field(..., alias="class", example="Economy")
    duration: float = Field(..., example=2.25)
    days_left: int = Field(..., example=15)

    class Config:
        populate_by_name = True


@app.post("/predict")
def predict_price(data: FlightInput):
    # Data ko dictionary mein convert karke alias key ('class') retain karna
    input_dict = data.model_dump(by_alias=True)

    # DataFrame banana jaisa model pipeline expect karta hai
    input_df = pd.DataFrame([input_dict])

    # Prediction
    prediction = loaded_model.predict(input_df)
    predicted_price = round(float(prediction[0]), 2)

    return {
        "status": "success",
        "predicted_price_inr": predicted_price,
        "currency": "INR (₹)"
    }


@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Flight Price Prediction API is running successfully!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": loaded_model is not None
    }