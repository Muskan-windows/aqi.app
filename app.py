import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="AQI Guardian", layout="wide")

# ---------------------------
# TITLE
# ---------------------------
st.title("🌍 AQI Guardian - Smart Air Quality Predictor")
st.markdown("Monitor pollution, visualize trends & predict AQI")

# ---------------------------
# MODE SELECTION
# ---------------------------
st.subheader("⚙️ Select Input Method")

mode = st.radio(
    "Choose how you want to proceed:",
    ["📂 Upload Dataset", "✍️ Manual Input"]
)

# ---------------------------
# FILE UPLOAD
# ---------------------------
df = None

if mode == "📂 Upload Dataset":
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("Dataset loaded successfully!")
        st.dataframe(df.head())

# ---------------------------
# MANUAL INPUT
# ---------------------------
if mode == "✍️ Manual Input":
    st.subheader("Enter Pollution Values")

    col1, col2, col3 = st.columns(3)

    with col1:
        pm25 = st.number_input("PM2.5", 0.0, 500.0, 50.0)

    with col2:
        pm10 = st.number_input("PM10", 0.0, 500.0, 80.0)

    with col3:
        no2 = st.number_input("NO2", 0.0, 200.0, 40.0)

# ---------------------------
# PREDICT BUTTON
# ---------------------------
if st.button("🚀 Predict AQI"):

    st.success("Prediction Generated!")

    # ---------------------------
    # HANDLE DATA
    # ---------------------------
    if df is None:
        # fallback dataset
        df = pd.DataFrame({
            "PM2.5": np.random.randint(20, 200, 50),
            "PM10": np.random.randint(30, 250, 50),
            "NO2": np.random.randint(10, 100, 50),
            "AQI": np.random.randint(50, 300, 50)
        })

    # ---------------------------
    # AQI CALCULATION (ONLY IF MANUAL)
    # ---------------------------
    if mode == "✍️ Manual Input":
        aqi = (pm25 * 0.5 + pm10 * 0.3 + no2 * 0.2)
    else:
        aqi = df["AQI"].mean()

    # ---------------------------
    # AQI STATUS
    # ---------------------------
    if aqi <= 50:
        status = "🟢 Good"
    elif aqi <= 100:
        status = "🟡 Moderate"
    else:
        status = "🔴 Unhealthy"

    st.metric("🌫 Predicted AQI", round(aqi, 2))
    st.write(f"### Status: {status}")

    # ---------------------------
    # GRAPH
    # ---------------------------
    st.caption("📊 Visualizing historical AQI trends")
    st.subheader("📈 AQI Trend")

    if "AQI" in df.columns:
        fig, ax = plt.subplots()
        ax.plot(df["AQI"])
        ax.set_title("AQI Over Time")
        st.pyplot(fig)
    else:
        st.warning("No AQI column found in dataset!")

    # ---------------------------
    # MAP
    # ---------------------------
    st.subheader("🗺 AQI Location Map")

    map_data = pd.DataFrame({
        "lat": [28.61],
        "lon": [77.23]
    })

    st.map(map_data)

    # ---------------------------
    # DATA PREVIEW
    # ---------------------------
    st.subheader("📊 Dataset Preview")
    st.dataframe(df.head())