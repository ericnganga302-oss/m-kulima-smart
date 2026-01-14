# smart/engine/data_loader.py
import streamlit as st
from st_supabase_connection import SupabaseConnection
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# 🛡️ SOVEREIGN DATA CONNECTION
# ---------------------------------------------------------
def get_db():
    """Initializes connection to the Supabase Cloud Ledger."""
    return st.connection("supabase", type=SupabaseConnection)

def init_db():
    """
    NOTE: In Supabase, tables are created via the SQL Editor on their website.
    Use the SQL provided below in the Supabase dashboard.
    """
    pass 

# ---------- INGESTION (Pushing to Cloud) ----------

def add_animal(animal_id, species, birth_date):
    db = get_db()
    data = {
        "animal_id": animal_id, 
        "species": species, 
        "birth_date": str(birth_date)
    }
    # Using upsert (INSERT OR UPDATE) to prevent duplicates
    db.table("animals").upsert(data).execute()

def add_weight(animal_id, weight):
    db = get_db()
    data = {
        "animal_id": animal_id, 
        "weight": float(weight), 
        "date": datetime.now().isoformat()
    }
    db.table("weights").insert(data).execute()

def add_health(animal_id, temperature, activity):
    db = get_db()
    data = {
        "animal_id": animal_id, 
        "temperature": float(temperature), 
        "activity": int(activity), 
        "date": datetime.now().isoformat()
    }
    db.table("health").insert(data).execute()

# ---------- LOADERS (Pulling from Cloud) ----------

def load_weight_history(animal_id):
    db = get_db()
    # Query the 'weights' table for specific animal
    response = db.table("weights").select("weight, date").eq("animal_id", animal_id).order("date").execute()
    
    # Convert response to Pandas DataFrame for your Plotly charts
    df = pd.DataFrame(response.data)
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
    return df

def load_health_latest(animal_id):
    db = get_db()
    # Pull only the most recent record
    response = db.table("health").select("temperature, activity, date").eq("animal_id", animal_id).order("date", desc=True).limit(1).execute()
    
    return pd.DataFrame(response.data)


def load_weight_history(animal_id):
    db = get_db()
    # Fetch real data from the weights table
    response = db.table("weights").select("weight, date").eq("animal_id", animal_id).order("date").execute()
    df = pd.DataFrame(response.data)
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
    return df