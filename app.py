import streamlit as st
from datetime import date


# -----------------------------
# ENGINE IMPORTS
# -----------------------------
from smart.engine.inference import forecast_growth, health_status
from smart.engine.data_loader import (
    add_animal,
    load_weight_history,
)
from smart.engine.ingest import (
    ingest_weight_csv,
    ingest_sensor_csv,
)
from smart.engine.explain import explain_growth

from smart.training.scheduler import start_scheduler

start_scheduler()


# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="M-Kulima Smart",
    layout="wide"
)

# -----------------------------
# PAGE FUNCTIONS
# -----------------------------

def page_register():
    st.header("🐄 Register Animal")

    animal_id = st.text_input("Animal ID (unique)")
    species = st.selectbox("Species", ["Cattle", "Goat", "Sheep"])
    dob = st.date_input("Date of Birth", max_value=date.today())

    if st.button("Register Animal"):
        if not animal_id:
            st.error("Animal ID is required")
            return

        try:
            add_animal(animal_id, species, str(dob))
            st.success("Animal registered successfully")
        except Exception as e:
            st.warning("Animal already exists or invalid data")


def page_growth():
    st.header("📈 Growth Forecast")

    animal_id = st.text_input("Animal ID")

    if not animal_id:
        st.info("Enter an animal ID to continue")
        return

    weights = load_weight_history(animal_id)

    if len(weights) < 3:
        st.warning("Not enough historical weight data")
        return

    prediction = forecast_growth(animal_id)
    explanation = explain_growth(weights)

    st.subheader("Predicted Growth")
    st.metric("Next Weight (kg)", round(prediction, 2))

    st.subheader("Model Explanation")
    st.write(f"**Trend:** {explanation['trend']}")
    st.write(f"**Growth Rate:** {explanation['rate']} kg/day")
    st.write(f"**Confidence:** {explanation['confidence']}")


def page_health():
    st.header("🩺 Health Monitor")

    temp = st.number_input("Temperature (°C)", 35.0, 45.0, 38.5)
    activity = st.number_input("Activity Level", 0, 200, 100)

    status = health_status({
        "temperature": temp,
        "activity": activity
    })

    if status == "NORMAL":
        st.success("Animal status: NORMAL")
    elif status == "WARNING":
        st.warning("Animal status: WARNING")
    else:
        st.error("Animal status: CRITICAL")


def page_carbon():
    st.header("♻️ Carbon Credits")

    animals = st.number_input("Number of Animals", 1, 1000, 10)
    credits = animals * 0.5

    st.metric("Estimated Carbon Credits", credits)


def page_data_ingestion():
    st.header("📥 Data Ingestion")

    st.subheader("Upload Weight Data (CSV)")
    weight_file = st.file_uploader(
        "Weights CSV",
        type=["csv"],
        key="weights"
    )

    if weight_file and st.button("Ingest Weights"):
        try:
            ingest_weight_csv(weight_file)
            st.success("Weight data ingested successfully")
        except Exception as e:
            st.error(f"Ingestion failed: {e}")

    st.divider()

    st.subheader("Upload Sensor Data (CSV)")
    sensor_file = st.file_uploader(
        "Sensor CSV",
        type=["csv"],
        key="sensors"
    )

    if sensor_file and st.button("Ingest Sensors"):
        try:
            ingest_sensor_csv(sensor_file)
            st.success("Sensor data ingested successfully")
        except Exception as e:
            st.error(f"Ingestion failed: {e}")


# -----------------------------
# PAGE REGISTRY 
# -----------------------------
PAGES = {
    "Register Animal": page_register,
    "Growth Forecast": page_growth,
    "Health Monitor": page_health,
    "Carbon Credits": page_carbon,
    "Data Ingestion": page_data_ingestion,
}

# -----------------------------
# NAVIGATION
# -----------------------------
st.sidebar.title("M-Kulima Smart")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

PAGES[selection]()
