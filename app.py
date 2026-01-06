import streamlit as st
from datetime import date

# -------------------- ENGINE IMPORTS --------------------
from smart.engine.data_loader import (
    add_animal,
    add_weight,
    add_health
)

from smart.engine.inference import (
    forecast_growth,
    health_status
)

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="M-Kulima Smart",
    layout="wide"
)

st.title("🐄 M-Kulima Smart Livestock Intelligence")

# -------------------- SIDEBAR NAV --------------------
nav = st.sidebar.radio(
    "Navigation",
    [
        "Animal Registration",
        "Weight Tracking",
        "Health Monitoring",
        "Growth Prediction"
    ]
)

# -------------------- SHARED INPUT --------------------
st.sidebar.divider()
animal_id = st.sidebar.text_input("Animal ID", value="AEG-001")

# =====================================================
# 🟢 1. ANIMAL REGISTRATION
# =====================================================
if nav == "Animal Registration":
    st.header("📋 Register Animal")

    species = st.selectbox("Species", ["Cattle", "Goat", "Sheep", "Poultry"])
    dob = st.date_input("Date of Birth", value=date(2024, 1, 1))

    if st.button("Register Animal"):
        try:
            add_animal(animal_id, species, str(dob))
            st.success(f"Animal {animal_id} registered successfully")
        except Exception as e:
            st.error(f"Error: {e}")

# =====================================================
# 🟢 2. WEIGHT TRACKING (STEP 2.3 ✔)
# =====================================================
elif nav == "Weight Tracking":
    st.header("⚖️ Record Weight")

    weight = st.number_input(
        "Current Weight (kg)",
        min_value=0.0,
        step=0.5
    )

    if st.button("Save Weight"):
        try:
            add_weight(animal_id, weight)
            st.success("Weight saved successfully")
        except Exception as e:
            st.error(f"Error: {e}")

# =====================================================
# 🟢 3. HEALTH MONITORING (STEP 2.3 ✔)
# =====================================================
elif nav == "Health Monitoring":
    st.header("🌡 Health Monitoring")

    temperature = st.slider("Body Temperature (°C)", 35.0, 42.0, 38.5)
    activity = st.slider("Activity Level", 0, 100, 60)

    if st.button("Save Health Data"):
        try:
            add_health(animal_id, temperature, activity)
            st.success("Health data recorded")
        except Exception as e:
            st.error(f"Error: {e}")

    st.divider()

    try:
        status = health_status(animal_id)
        st.subheader(f"Health Status: {status}")
    except Exception as e:
        st.warning("Not enough data for health analysis yet")

# =====================================================
# 🟢 4. GROWTH PREDICTION (REAL DATA)
# =====================================================
elif nav == "Growth Prediction":
    st.header("📈 Growth Forecast")

    days_ahead = st.slider("Forecast Days", 7, 90, 30)

    if st.button("Run Forecast"):
        try:
            predictions = forecast_growth(animal_id, days_ahead)
            st.line_chart(predictions)
            st.success("Forecast generated from real weight history")
        except Exception as e:
            st.error("Not enough weight data to forecast yet")
