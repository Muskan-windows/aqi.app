import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide")

# ---------------- TITLE ----------------
st.title("🌍 AQI Guardian - Smart Air Quality Predictor")

st.markdown("""
Monitor air pollution, visualize trends, and predict AQI using Machine Learning.
""")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

# Upload OR default
uploaded_file = st.file_uploader("📂 Upload your dataset (optional)", type=["csv"])

if uploaded_file:
    df = load_data(uploaded_file)
else:
    df = load_data("aqi.csv")  # default file

# ---------------- BASIC CHECK ----------------
if df is None or df.empty:
    st.error("Dataset is empty ❌")
    st.stop()

# Limit size for performance
if len(df) > 2000:
    df = df.sample(1000)

# ---------------- CITY DROPDOWN ----------------
if 'city' in df.columns:
    city = st.selectbox("🏙️ Select City", df['city'].unique())
    df_city = df[df['city'] == city]
else:
    df_city = df

# ---------------- DATA PREVIEW ----------------
with st.expander("📊 View Dataset"):
    st.dataframe(df_city.head(50))

# ---------------- AQI METRICS ----------------
if 'aqi_index' in df_city.columns:
    avg_aqi = df_city['aqi_index'].mean()
    max_aqi = df_city['aqi_index'].max()

    col1, col2 = st.columns(2)
    col1.metric("Average AQI", round(avg_aqi, 2))
    col2.metric("Max AQI", int(max_aqi))

    # AQI COLOR STATUS
    if avg_aqi <= 50:
        st.success("🟢 Good Air Quality")
    elif avg_aqi <= 100:
        st.warning("🟡 Moderate Air Quality")
    else:
        st.error("🔴 Unhealthy Air")

# ---------------- GRAPHS ----------------
st.subheader("📈 Pollution Trends")

if all(col in df_city.columns for col in ['pm2_5', 'pm10']):
    st.line_chart(df_city[['pm2_5', 'pm10']])

# ---------------- MAP ----------------
st.subheader("🗺️ Pollution Map")

if 'lat' in df_city.columns and 'lon' in df_city.columns:
    st.map(df_city[['lat', 'lon']])
else:
    st.info("Latitude & Longitude not available")

# ---------------- MODEL ----------------
@st.cache_data
def train_model(X, y):
    model = LinearRegression()
    model.fit(X, y)
    return model

features = ['pm2_5', 'pm10', 'no2', 'co']
target = 'aqi_index'

if all(col in df_city.columns for col in features + [target]):

    df_model = df_city[features + [target]].dropna()

    if len(df_model) > 10:

        X = df_model[features]
        y = df_model[target]

        model = train_model(X, y)

        st.success("🤖 Model trained successfully")

        # ---------------- PREDICTION ----------------
        st.subheader("🔮 Predict AQI")

        col1, col2 = st.columns(2)

        with col1:
            pm25 = st.number_input("PM2.5", value=50.0)
            pm10 = st.number_input("PM10", value=80.0)

        with col2:
            no2 = st.number_input("NO2", value=30.0)
            co = st.number_input("CO", value=1.0)

        if st.button("Predict AQI"):

            input_data = [[pm25, pm10, no2, co]]
            pred = model.predict(input_data)[0]

            st.subheader(f"Predicted AQI: {round(pred, 2)}")

            # Prediction AQI Status
            if pred <= 50:
                st.success("🟢 Good Air Quality")
            elif pred <= 100:
                st.warning("🟡 Moderate Air Quality")
            else:
                st.error("🔴 Unhealthy Air")

    else:
        st.warning("Not enough data to train model")

else:
    st.warning("Required columns missing for ML")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("Built for Hackathon 🚀 | AI + Data for Cleaner Air")