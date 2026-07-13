import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

st.set_page_config(layout="wide")

# Load data (default + optional upload)
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

# 🎯 ONLY ONE uploader (correct way)
uploaded_file = st.file_uploader("Upload CSV (optional)", type=["csv"])

if uploaded_file is not None:
    df = load_data(uploaded_file)
else:
    df = load_data("delhi-weather-aqi-2025.csv")  # ✅ your file name

# ✅ Cache model
@st.cache_data
def train_model(X, y):
    model = LinearRegression()
    model.fit(X, y)
    return model

# 🌟 UI
st.title("AQI Guardian 🤖")

st.markdown("""
### 🌍 Problem
Air pollution is a major health risk. People don’t know real-time air quality.

### 💡 Solution
This app predicts AQI and helps users understand pollution trends using AI.
""")

# Graph Preview
st.subheader("Dataset Preview")
st.dataframe(df.head(50))

#  City filter
if 'city' in df.columns:
    city = st.selectbox("Select City", df['city'].unique())
    df = df[df['city'] == city]

# 📊 Graphs
st.subheader("📊 Air Quality Trends")
if 'pm2_5' in df.columns and 'pm10' in df.columns:
    st.line_chart(df[['pm2_5', 'pm10']])

# 🌍 AQI Status
if 'aqi_index' in df.columns:
    avg_aqi = df['aqi_index'].mean()

    col1, col2 = st.columns(2)
    col1.metric("Avg AQI", round(avg_aqi, 2))
    col2.metric("Max AQI", int(df['aqi_index'].max()))

    if avg_aqi <= 50:
        st.success("🟢 Good Air Quality")
    elif avg_aqi <= 100:
        st.warning("🟡 Moderate Air Quality")
    else:
        st.error("🔴 Unhealthy Air")

# 🤖 Model
features = ['pm2_5', 'pm10', 'no2', 'co']
target = 'aqi_index'

if all(col in df.columns for col in features + [target]):

    df_model = df[features + [target]].dropna()

    if len(df_model) > 10:
        X = df_model[features]
        y = df_model[target]

        model = train_model(X, y)

        st.success("Model trained successfully ✅")

        # 🔮 Prediction
        st.subheader("🔮 Predict Your Own AQI")

        pm25 = st.number_input("PM2.5", value=10.0)
        pm10 = st.number_input("PM10", value=20.0)
        no2 = st.number_input("NO2", value=15.0)
        co = st.number_input("CO", value=0.5)

        if st.button("Predict AQI"):
            input_data = [[pm25, pm10, no2, co]]
            pred = model.predict(input_data)
            st.success(f"Predicted AQI: {round(pred[0], 2)}")

# 🗺️ Map
st.subheader("🗺️ Pollution Map")
if 'lat' in df.columns and 'lon' in df.columns:
    st.map(df[['lat', 'lon']])