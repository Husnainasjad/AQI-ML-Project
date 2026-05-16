import requests
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")

# Karachi coordinates
LAT = 24.8607
LON = 67.0011

# API URL
url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY}"

# Send request
response = requests.get(url)

# Convert response to JSON
data = response.json()

# Extract AQI data
aqi_data = data["list"][0]

main_data = aqi_data["main"]
components = aqi_data["components"]

# Current timestamp
current_time = datetime.now()

# Create dataframe
df = pd.DataFrame({
    "Timestamp": [current_time],
    "AQI": [main_data["aqi"]],
    "CO": [components["co"]],
    "NO2": [components["no2"]],
    "O3": [components["o3"]],
    "PM2.5": [components["pm2_5"]],
    "PM10": [components["pm10"]],
})

# File path
file_path = "data/aqi_data.csv"

# Append data if file exists
if os.path.exists(file_path):
    df.to_csv(file_path, mode='a', header=False, index=False)
else:
    df.to_csv(file_path, index=False)

print("Data saved successfully!")
print(df)
