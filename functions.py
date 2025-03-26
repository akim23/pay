import base64
import pandas as pd
import os
import streamlit as st

# Function to load graph data from CSV
def load_graph_data():
    if os.path.exists('graph_data.csv'):
        df = pd.read_csv('graph_data.csv')
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        return df.to_dict('records')
    return []

# Function to save graph data to CSV
def save_graph_data(data):
    if data:
        df = pd.DataFrame(data)
        df.to_csv('graph_data.csv', index=False)

# Function to add or update job entry
def add_or_update_entry(job_type, hours, rate, cash_tips, card_tips):
    total_tips = cash_tips + card_tips
    hourly_tips = total_tips / hours if hours > 0 else 0
    hourly_earnings = (hours * rate + total_tips) / hours if hours > 0 else 0  # Hourly earnings including tips
    total_pay = (hours * rate) + total_tips

    # Add new entry with date
    st.session_state.work_data.append({
        "Job Type": job_type,
        "Hours Worked": hours,
        "Hourly Rate": rate,
        "Cash Tips": cash_tips,
        "Card Tips": card_tips,
        "Total Tips": total_tips,
        "Hourly Tips": hourly_tips,
        "Hourly Earnings": hourly_earnings,
        "Total Earnings": total_pay
    })

# Function to encode an image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Function to encode audio to base64
def get_audio_base64(audio_path):
    with open(audio_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode()
