import streamlit as st
from datetime import date
import pandas as pd
import plotly.graph_objects as go
import speech_recognition as sr  # REAL Speech Processing
from st_supabase_connection import SupabaseConnection
import re

# Import your custom modules
from smart.engine.data_loader import (
    add_animal,
    add_weight,
    add_health,
    load_weight_history
)
from smart.engine.inference import (
    forecast_growth,
    health_status,
    disease_prediction
)
from smart.training.scheduler import start_scheduler

# ---------------------------------------------------------
# 🛡️ SYSTEM CORE: SINGLETON SCHEDULER
# ---------------------------------------------------------
@st.cache_resource
def init_aegis_engine():
    try:
        start_scheduler()
        return "🟢 AI NODES ONLINE"
    except Exception:
        return "🟡 ENGINE ACTIVE"

engine_status = init_aegis_engine()

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="M-Kulima Smart",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS for a professional "Sovereign" look
st.markdown("""
    <style>
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    [data-testid="stSidebar"] { background-color: #0e1117; }
    .stAudioInput { width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ M-Kulima Smart Livestock Intelligence")

# -------------------- REAL VOICE PROCESSING ENGINE --------------------
def process_voice_command(audio_bytes):
    """
    REAL DATA PROCESSING: 
    Takes raw audio bytes -> Saves Temp File -> Sends to Google Speech API -> Returns Text
    """
    r = sr.Recognizer()
    
    # 1. Save bytes to a temporary file for the recognizer to read
    with open("temp_command.wav", "wb") as f:
        f.write(audio_bytes.read())
        
    # 2. Process the file (REAL API CALL)
    try:
        with sr.AudioFile("temp_command.wav") as source:
            audio_data = r.record(source)
            # Uses Google's free speech API (Real, not simulated)
            text = r.recognize_google(audio_data)
            return text, None
    except sr.UnknownValueError:
        return None, "Audio unclear. Please speak closer to the mic."
    except sr.RequestError:
        return None, "Connection to Neural Net lost (Check Internet)."

# -------------------- SIDEBAR NAV & VOICE NODE --------------------
st.sidebar.title("AEGIS CONTROL")
st.sidebar.caption(engine_status)

# --- NEW: VOICE COMMAND NODE ---
with st.sidebar.expander("🎙️ VOICE COMMAND NODE", expanded=True):
    # This is the NEW native component
    voice_input = st.audio_input("Execute Verbal Command")

    if voice_input:
        st.info("Processing Signal...")
        command_text, error = process_voice_command(voice_input)
        
        if error:
            st.error(error)
        else:
            st.success(f"🗣️: '{command_text}'")
            # BASIC INTELLIGENCE PARSER (Extracts numbers)
            # If you say "Weight is 450", it finds "450"
            extracted_numbers = re.findall(r"[-+]?\d*\.\d+|\d+", command_text)
            if extracted_numbers:
                st.session_state['voice_val'] = float(extracted_numbers[0])
                st.caption(f"⚡ Value Extracted: {st.session_state['voice_val']}")

nav = st.sidebar.radio(
    "Navigation",
    [
        "Animal Registration",
        "Weight Tracking",
        "Health Monitoring",
        "Growth Prediction"
    ]
)

st.sidebar.divider()
animal_id = st.sidebar.text_input("Active Animal ID", value="AEG-001")
st.sidebar.info("System Node: UoN-Nakuru-01")

# =====================================================
# 🟢 1. ANIMAL REGISTRATION
# =====================================================
if nav == "Animal Registration":
    st.header("📋 Sovereign Asset Registration")
    
    col1, col2 = st.columns(2)
    with col1:
        species = st.selectbox("Species", ["Cattle", "Goat", "Sheep", "Poultry"])
        dob = st.date_input("Date of Birth", value=date(2024, 1, 1))

    if st.button("Register to Ledger"):
        try:
            add_animal(animal_id, species, str(dob))
            st.success(f"✅ Animal {animal_id} locked to sovereign database.")
        except Exception as e:
            st.error(f"Error: {e}")

# =====================================================
# 🟢 2. WEIGHT TRACKING
# =====================================================
elif nav == "Weight Tracking":
    st.header("⚖️ Precision Weight Analytics")

    # AUTO-FILL FROM VOICE
    # If the voice engine found a number, we autofill it here
    default_weight = st.session_state.get('voice_val', 0.0)

    col1, col2 = st.columns([1, 2])
    with col1:
        weight = st.number_input("Current Weight (kg)", min_value=0.0, step=0.5, value=float(default_weight))
        
        if default_weight > 0:
            st.caption("✨ Value autofilled from Voice Command")

        if st.button("Commit Weight"):
            try:
                add_weight(animal_id, weight)
                st.success("💾 Telemetry Saved")
                # Clear the voice memory
                if 'voice_val' in st.session_state: del st.session_state['voice_val']
            except Exception as e:
                st.error(f"Error: {e}")
    
    with col2:
        h_weights = load_weight_history(animal_id)
        if h_weights is not None and len(h_weights) > 0:
            st.line_chart(h_weights)

# =====================================================
# 🟢 3. HEALTH MONITORING
# =====================================================
elif nav == "Health Monitoring":
    st.header("🌡 Sentinel Health & Diagnostic AI")

    # AUTO-FILL FROM VOICE
    default_val = st.session_state.get('voice_val', 38.5)

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Signal Input")
        temperature = st.slider("Body Temperature (°C)", 35.0, 42.0, float(default_val) if 35 <= default_val <= 42 else 38.5)
        
        if 35 <= default_val <= 42:
             st.caption("✨ Temperature autofilled from Voice Command")

        activity = st.slider("Activity Level (Steps/Hr)", 0, 100, 60)

        if st.button("Log Signals"):
            try:
                add_health(animal_id, temperature, activity)
                st.toast("Biometric pulse recorded")
                if 'voice_val' in st.session_state: del st.session_state['voice_val']
            except Exception as e:
                st.error(f"Error: {e}")

    with col2:
        st.subheader("AI Inference")
        status_payload = health_status({
            "animal_id": animal_id,
            "temperature": temperature,
            "activity": activity
        })
        
        if status_payload["risk"] == "low":
            st.success(f"Pulse Status: {status_payload['status'].upper()}")
        elif status_payload["risk"] == "medium":
            st.warning(f"Pulse Status: {status_payload['status'].upper()}")
        else:
            st.error(f"Pulse Status: {status_payload['status'].upper()}")
        
        st.write(f"**Advisor:** {status_payload['message']}")

    st.divider()

    st.subheader("🩺 Diagnostic Deep Scan")
    if st.button("Run Disease Inference"):
        diag = disease_prediction(animal_id)
        if "diagnosis" in diag:
            c1, c2 = st.columns(2)
            with c1:
                st.info(f"🔍 **Symptoms Detected:** {', '.join(diag['symptoms_detected'])}")
                st.markdown(f"### Probable Cause: **{diag['diagnosis']['disease']}**")
            with c2:
                st.warning(f"💊 **Vet Action:** {diag['diagnosis']['action']}")
        else:
            st.warning("Insufficient signal history for a high-confidence diagnosis.")

# =====================================================
# 🟢 4. GROWTH PREDICTION
# =====================================================
elif nav == "Growth Prediction":
    st.header("📈 Growth Trajectory Forecast")

    days_ahead = st.slider("Forecast Horizon (Days)", 7, 90, 30)

    if st.button("Generate AI Forecast"):
        try:
            result = forecast_growth(animal_id, days_ahead)
            
            if result["status"] != "insufficient_data":
                m1, m2 = st.columns(2)
                m1.metric("Predicted Weight", f"{result['prediction'][-1]:.2f} kg")
                m2.metric("Target Weight ETA", f"{result['eta_days'] if result['eta_days'] else 'Beyond Window'} Days")
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(y=result["prediction"], mode='lines', name='Trajectory', line=dict(color='#238636', width=4)))
                fig.update_layout(title="Future Weight Projection", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
                
            else:
                st.error(result["message"])
        except Exception as e:
            st.error(f"System Error: {e}")

# -------------------- FOOTER --------------------
st.divider()
st.caption("© 2026 M-Kulima Smart | M-kulima Smart  System Architecture | Developed by Eric Kamau")