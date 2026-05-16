from fastapi import FastAPI
import joblib
import numpy as np
from pydantic import BaseModel

app = FastAPI()

# Load models
model = joblib.load("models/aqi_model.pkl")
scaler = joblib.load("models/scaler.pkl")
encoder = joblib.load("models/encoder.pkl")

# Input schema
class AQIData(BaseModel):
    co: float
    ozone: float
    no2: float
    pm25: float

@app.get("/")
def home():
    return {"message": "AQI API Running"}

@app.post("/predict")
def predict(data: AQIData):

    input_data = np.array([[
        data.co,
        data.ozone,
        data.no2,
        data.pm25
    ]])

    scaled = scaler.transform(input_data)

    prediction = model.predict(scaled)

    result = encoder.inverse_transform(prediction)[0]

    return {
        "prediction": result
    }