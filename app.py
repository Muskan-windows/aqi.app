import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="AQI Guardian", layout="wide")

# ------------------ HEADER ------------------
st.title("🌍 AQI Guardian - Smart Air Quality Predictor")
st.markdown("Monitor pollution, visualize trends & predict AQI intelligently")

# ------------------ INPUT METHOD ------------------
st.subheader("⚙️ Select Input Method")

option = st.radio("Choose how you want to proceed:",
                  ("Upload CSV", "Manual Input"))

df = None

# ------------------ CSV UPLOAD ------------------
if option == "Upload CSV":
    file = st.file_uploader("Upload your dataset", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.success("Dataset loaded successfully!")
        st.write(df.head())

        # DEBUG: show columns
        st.write("Detected columns:", df.columns)

# ------------------ MANUAL INPUT ------------------
if option == "Manual Input":
    st.subheader("Enter Pollution Values")

    pm25 = st.number_input("PM2.5", value=50)
    pm10 = st.number_input("PM10", value=80)
    no2 = st.number_input("NO2", value=40)
    co = st.number_input("CO", value=1)

# ------------------ BUTTON ------------------
if st.button("🚀 Predict AQI"):

    # ---------- CASE 1: CSV ----------
    if df is not None:

        # Normalize column names
        df.columns = [col.strip().lower() for col in df.columns]

        # ---------------------------
        # AUTO DETECT COLUMNS
        # ---------------------------
        def find_col(keywords):
            for col in df.columns:
                for key in keywords:
                    if key in col:
                        return col
            return None

        pm25_col = find_col(["pm2.5", "pm25", "pm_2_5", "pm2_5"])
        pm10_col = find_col(["pm10", "pm_10"])
        no2_col = find_col(["no2", "no_2"])

        if pm25_col and pm10_col and no2_col:

            st.success(f"Using columns: {pm25_col}, {pm10_col}, {no2_col}")

            # Create AQI column
            df["aqi"] = (
                df[pm25_col] * 0.5 +
                df[pm10_col] * 0.3 +
                df[no2_col] * 0.2
            )

            avg_aqi = df["aqi"].mean()
            st.metric("Average AQI", round(avg_aqi, 2))

            # ---------- STATUS ----------
            if avg_aqi <= 50:
                status = "🟢 Good"
            elif avg_aqi <= 100:
                status = "🟡 Moderate"
            elif avg_aqi <= 200:
                status = "🟠 Poor"
            else:
                status = "🔴 Very Poor"

            st.subheader(f"AQI Status: {status}")

            # ---------- GRAPH ----------
            st.subheader("📈 AQI Trend")

            fig, ax = plt.subplots()
            ax.plot(df["aqi"], marker='o')
            ax.set_xlabel("Index")
            ax.set_ylabel("AQI")
            ax.set_title("AQI Trend Over Time")
            st.pyplot(fig)

            # ---------- MAP ----------
            st.subheader("🗺️ Location Map")

            lat_col = find_col(["lat", "latitude"])
            lon_col = find_col(["lon", "longitude"])

            if lat_col and lon_col:
                map_df = df[[lat_col, lon_col]].rename(
                    columns={lat_col: "lat", lon_col: "lon"}
                )
                st.map(map_df)
            else:
                # Default Delhi
                map_df = pd.DataFrame({
                    "lat": [28.61],
                    "lon": [77.23]
                })
                st.map(map_df)

        else:
            st.error("❌ Could not detect required columns (PM2.5, PM10, NO2)")
            st.stop()

    # ---------- CASE 2: MANUAL ----------
    else:
        st.success("Prediction Generated!")

        aqi = (pm25 * 0.5) + (pm10 * 0.3) + (no2 * 0.1) + (co * 10)

        st.metric("Predicted AQI", round(aqi, 2))

        if aqi <= 50:
            status = "🟢 Good"
        elif aqi <= 100:
            status = "🟡 Moderate"
        elif aqi <= 200:
            status = "🟠 Poor"
        else:
            status = "🔴 Very Poor"

        st.subheader(f"AQI Status: {status}")

        # ---------- GRAPH ----------
        st.subheader("📊 Pollution Breakdown")

        pollutants = ["PM2.5", "PM10", "NO2", "CO"]
        values = [pm25, pm10, no2, co]

        fig, ax = plt.subplots()
        ax.bar(pollutants, values)
        st.pyplot(fig)

        # ---------- MAP ----------
        st.subheader("🗺️ Location Map")
        map_df = pd.DataFrame({
            "lat": [28.61],
            "lon": [77.23]
        })
        st.map(map_df)