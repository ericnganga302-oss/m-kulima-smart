import streamlit as st
from datetime import date

# -----------------------------
# ENGINE IMPORTS
# -----------------------------
# These imports assume you have your folders set up as: 
# smart/engine/inference.py, smart/engine/data_loader.py, etc.

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

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="M-Kulima Smart",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------
# BACKGROUND SERVICES (THE FIX)
# -----------------------------
# @st.cache_resource ensures this runs ONLY ONCE per server session.
# This prevents the "SchedulerAlreadyRunningError" crash.
@st.cache_resource
def init_background_services():
    try:
        start_scheduler()
        return "✅ AI Scheduler Active"
    except Exception as e:
        return f"⚠️ Scheduler Status: {e}"

# Initialize the background intelligence
service_status = init_background_services()

# -----------------------------
# PAGE FUNCTIONS
# -----------------------------

def page_register():
    st.header("🐄 Register New Animal")
    st.caption("Add a new asset to your sovereign ledger.")

    with st.form("register_form"):
        animal_id = st.text_input("Animal ID (Unique)", placeholder="e.g., KES-001")
        species = st.selectbox("Species", ["Cattle", "Goat", "Sheep", "Poultry"])
        dob = st.date_input("Date of Birth", max_value=date.today())
        
        submitted = st.form_submit_button("Register Asset")

        if submitted:
            if not animal_id:
                st.error("❌ Animal ID is required.")
                return

            try:
                # Assuming add_animal is defined in your data_loader
                add_animal(animal_id, species, str(dob))
                st.success(f"✅ Asset {animal_id} registered successfully!")
            except Exception as e:
                st.error(f"❌ Registration Failed: {e}")


def page_growth():
    st.header("📈 Growth & Market Forecast")
    st.caption("Predict future weight to optimize selling time.")

    animal_id = st.text_input("Enter Animal ID for Analysis")

    if not animal_id:
        st.info("👋 Enter an Animal ID to see predictions.")
        return

    # Load data from your database
    weights = load_weight_history(animal_id)

    if not weights or len(weights) < 3:
        st.warning("⚠️ Insufficient Data: This animal needs at least 3 weight records to generate a forecast.")
        st.write("👉 Go to **Data Ingestion** to upload more records.")
        return

    # Run AI Inference
    try:
        prediction = forecast_growth(animal_id)
        explanation = explain_growth(weights)

        # Display Results
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Predicted Next Weight")
            st.metric("Forecast", f"{prediction:.2f} kg", delta=f"{explanation['rate']:.2f} kg/day")
        
        with col2:
            st.subheader("Intelligence Report")
            st.write(f"**Trend:** {explanation['trend']}")
            st.write(f"**Confidence:** {explanation['confidence']}")
            
        st.info("💡 **Advisor:** " + ("Sell now for max profit." if explanation['trend'] == "High Growth" else "Keep feeding; growth potential high."))
            
    except Exception as e:
        st.error(f"Prediction Error: {e}")


def page_health():
    st.header("🩺 Sentinel Health Monitor")
    st.caption("Real-time disease risk assessment.")

    col1, col2 = st.columns(2)
    with col1:
        temp = st.number_input("Body Temperature (°C)", 35.0, 43.0, 38.5)
    with col2:
        activity = st.number_input("Activity Level (Steps/Day)", 0, 20000, 5000)

    # Run Decision Intelligence
    status_result = health_status({
        "temperature": temp,
        "activity": activity
    })

    st.divider()
    
    # Display Logic
    if status_result == "NORMAL":
        st.success("✅ **Status: NORMAL** - Animal is healthy.")
    elif status_result == "WARNING":
        st.warning("⚠️ **Status: WARNING** - Monitor closely. Isolate if temp rises.")
    else: # CRITICAL
        st.error("🚨 **Status: CRITICAL** - High risk detected. Contact Vet immediately.")


def page_carbon():
    st.header("♻️ Carbon Credit Estimator")
    st.caption("Turn your efficient farming into revenue.")

    animals = st.number_input("Number of Cattle", 1, 1000, 10)
    
    # Simple logic for demo
    credits_per_animal = 0.5 # Tons of CO2e offset per efficient animal
    total_credits = animals * credits_per_animal
    est_value_kes = total_credits * 3000 # Approx 3000 KES per credit

    col1, col2 = st.columns(2)
    col1.metric("Estimated Carbon Credits", f"{total_credits} Tons")
    col2.metric("Potential Revenue (Yearly)", f"KES {est_value_kes:,.2f}")


def page_data_ingestion():
    st.header("📥 Data Ingestion Hub")
    st.caption("Upload CSV files to update the Sovereign Ledger.")

    tab1, tab2 = st.tabs(["⚖️ Weight Data", "📡 Sensor Data"])

    with tab1:
        st.subheader("Upload Weight Records")
        weight_file = st.file_uploader("Select Weights CSV", type=["csv"], key="weights")
        if weight_file and st.button("Ingest Weights"):
            try:
                ingest_weight_csv(weight_file)
                st.success("✅ Weight records locked to database.")
            except Exception as e:
                st.error(f"Ingestion failed: {e}")

    with tab2:
        st.subheader("Upload Sensor Streams")
        sensor_file = st.file_uploader("Select Sensor CSV", type=["csv"], key="sensors")
        if sensor_file and st.button("Ingest Sensors"):
            try:
                ingest_sensor_csv(sensor_file)
                st.success("✅ Sensor stream locked to database.")
            except Exception as e:
                st.error(f"Ingestion failed: {e}")


# -----------------------------
# NAVIGATION & SIDEBAR
# -----------------------------
PAGES = {
    "Register Animal": page_register,
    "Growth Forecast": page_growth,
    "Health Monitor": page_health,
    "Carbon Credits": page_carbon,
    "Data Ingestion": page_data_ingestion,
}

with st.sidebar:
    st.title("🛡️ M-Kulima Smart")
    st.caption(f"System Status: {service_status}")
    st.divider()
    selection = st.radio("Navigation", list(PAGES.keys()))
    st.divider()
    st.caption("© 2026 AEGIS Project | UoN")

# -----------------------------
# MAIN EXECUTION
# -----------------------------
if selection in PAGES:
    PAGES[selection]()