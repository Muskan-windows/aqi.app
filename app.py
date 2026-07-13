import streamlit as st
import pandas as pd
import numpy as np

st.title("🌍 AQI Prediction App")

# -------------------------------
# OPTION 1: Upload CSV (Optional)
# -------------------------------
uploaded_file = st.file_uploader("Upload CSV file (optional)", type=["csv"])

df = None

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("CSV uploaded successfully!")
    st.write(df.head())

# -------------------------------
# OPTION 2: Manual Input
# -------------------------------
st.subheader("Or Enter Values Manually")

pm25 = st.number_input("PM2.5", value=50.0)
pm10 = st.number_input("PM10", value=80.0)
no2 = st.number_input("NO2", value=30.0)
so2 = st.number_input("SO2", value=10.0)
co = st.number_input("CO", value=1.0)
o3 = st.number_input("O3", value=20.0)

# -------------------------------
# Prediction Button
# -------------------------------
if st.button("Predict AQI"):

    if uploaded_file is not None:
        st.info("Using uploaded CSV data")
        # Example: just show mean AQI (replace with your model)
        st.write("CSV Data Summary:")
        st.write(df.describe())

    else:
        st.info("Using manual input data")

        # Example calculation (replace with your ML model)
        aqi = (pm25 + pm10 + no2 + so2 + co + o3) / 6

        st.success(f"Predicted AQI: {aqi:.2f}")