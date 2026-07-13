import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="AQI Predictor", layout="wide")

# TITLE
st.title("🌍 AQI Prediction Dashboard")
st.subheader("By Your Name")

# OPTION
option = st.radio("Choose Input Method", ["Upload Dataset", "Manual Input"])

df = None

# FILE UPLOAD
if option == "Upload Dataset":
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip()
        st.success("Dataset Loaded Successfully!")

# MANUAL INPUT
else:
    pm25 = st.number_input("PM2.5")
    pm10 = st.number_input("PM10")
    no2 = st.number_input("NO2")

# BUTTON
if st.button("🚀 Predict AQI"):

    st.divider()

    # ---------- CASE 1: DATASET ----------
    if df is not None:

        st.subheader("📊 Dataset Preview")
        st.dataframe(df.head())

        # SIMPLE AQI (example logic)
        df["AQI"] = (df["PM2.5"] + df["PM10"] + df["NO2"]) / 3

        # STATUS
        def get_status(aqi):
            if aqi < 50:
                return "Good"
            elif aqi < 100:
                return "Moderate"
            else:
                return "Poor"

        df["Status"] = df["AQI"].apply(get_status)

        # SHOW CURRENT AQI
        latest_aqi = df["AQI"].iloc[-1]
        st.metric("Current AQI", round(latest_aqi, 2))

        # COLOR INDICATOR
        if latest_aqi < 50:
            st.success("🟢 Good Air Quality")
        elif latest_aqi < 100:
            st.warning("🟡 Moderate Air Quality")
        else:
            st.error("🔴 Poor Air Quality")

        # GRAPH
        st.subheader("📈 AQI Trend")

        chart_data = df.reset_index().rename(columns={"index": "day", "AQI": "aqi"})

        

        # MAP
        if "latitude" in df.columns and "longitude" in df.columns:
            st.subheader("🗺️ Location Map")
            st.map(df[["latitude", "longitude"]])

    # ---------- CASE 2: MANUAL ----------
    else:
        aqi = (pm25 + pm10 + no2) / 3

        st.metric("Predicted AQI", round(aqi, 2))

        if aqi < 50:
            st.success("🟢 Good")
        elif aqi < 100:
            st.warning("🟡 Moderate")
        else:
            st.error("🔴 Poor")

        st.info("Prediction based on simple formula (ML can be added)")