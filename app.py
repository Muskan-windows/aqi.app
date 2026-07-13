import streamlit as st
import pandas as pd
import numpy as np

st.title("🌍 AQI Prediction App")

# Upload option
uploaded_file = st.file_uploader("Upload CSV file (optional)", type=["csv"])

# Manual input
st.subheader("Or Enter Values Manually")

pm25 = st.number_input("PM2.5", value=50.0)
pm10 = st.number_input("PM10", value=80.0)
no2 = st.number_input("NO2", value=30.0)
so2 = st.number_input("SO2", value=10.0)
co = st.number_input("CO", value=1.0)
o3 = st.number_input("O3", value=20.0)

if st.button("Predict AQI"):

    # ---------------- CSV CASE ----------------
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.success("Using CSV Data")

        # GRAPH
        st.subheader("AQI Graph")
        st.line_chart(df.select_dtypes(include=np.number))

        # MAP (if lat/lon exists)
        if "lat" in df.columns and "lon" in df.columns:
            st.subheader("Location Map")
            st.map(df[["lat", "lon"]])

    # ---------------- MANUAL INPUT CASE ----------------
    else:
        st.success("Using Manual Input")

        # Create dataframe from input
        data = pd.DataFrame({
            "Pollutant": ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"],
            "Value": [pm25, pm10, no2, so2, co, o3]
        })

        # AQI calculation
        aqi = np.mean([pm25, pm10, no2, so2, co, o3])

        st.write(f"### Predicted AQI: {aqi:.2f}")

        # GRAPH (for manual input)
        st.subheader("Pollution Levels")
        st.bar_chart(data.set_index("Pollutant"))

        # FAKE MAP (since no location)
        st.subheader("Sample Location Map")
        map_data = pd.DataFrame({
            "lat": [28.61],   # Delhi example
            "lon": [77.20]
        })
        st.map(map_data)