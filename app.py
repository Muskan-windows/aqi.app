import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🌍 AQI Monitoring Dashboard")

# ---- AQI CATEGORY FUNCTION ----
def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good 😊"
    elif aqi <= 100:
        return "Moderate 😐"
    elif aqi <= 200:
        return "Unhealthy 😷"
    elif aqi <= 300:
        return "Very Unhealthy 🤢"
    else:
        return "Hazardous ☠️"

# ---- FILE UPLOAD ----
uploaded_file = st.file_uploader("Upload CSV (optional)", type=["csv"])

df = None

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")

# ---- USER INPUT ----
st.subheader("Or Enter Data Manually")

pm25 = st.number_input("PM2.5", value=50.0)
pm10 = st.number_input("PM10", value=80.0)
no2 = st.number_input("NO2", value=30.0)
lat = st.number_input("Latitude", value=28.61)
lon = st.number_input("Longitude", value=77.23)

# ---- CREATE DF IF USER INPUT ----
if not uploaded_file:
    df = pd.DataFrame({
        "pm2_5": [pm25],
        "pm10": [pm10],
        "no2": [no2],
        "latitude": [lat],
        "longitude": [lon]
    })

# ---- CALCULATE AQI ----
df["AQI"] = df[["pm2_5", "pm10", "no2"]].mean(axis=1)

# ---- SHOW DATA ----
st.subheader("📊 Data Preview")
st.write(df)

# ---- AQI RESULT ----
aqi_value = df["AQI"].iloc[0]
category = get_aqi_category(aqi_value)

st.subheader("🌡 AQI Result")
st.metric("AQI", round(aqi_value, 2))
st.success(f"Air Quality: {category}")

# ---- GRAPH ----
st.subheader("📈 Pollution Levels")

fig, ax = plt.subplots()
df[["pm2_5", "pm10", "no2"]].plot(kind="bar", ax=ax)
st.pyplot(fig)

# ---- MAP ----
st.subheader("🗺 Location Map")
st.map(df.rename(columns={"latitude": "lat", "longitude": "lon"}))