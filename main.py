import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
from functions import add_or_update_entry, load_graph_data, save_graph_data, get_audio_base64, image_to_base64

# Path to your local background image
image_path = "images/back1.jpg"
encoded_image = image_to_base64(image_path)

# Set background image
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('data:image/jpeg;base64,{encoded_image}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Path to title image
title_image_path = "images/KBC.webp"
st.image(title_image_path, use_container_width=True)

# Path to your audio file
audio_path = "Music/NewHorizons.mp3"

# Store music play state
if "is_playing" not in st.session_state:
    st.session_state.is_playing = False

# Function to generate HTML for autoplaying music (hidden)
def play_music():
    if not st.session_state.is_playing:
        st.session_state.is_playing = True
        audio_html = f"""
        <audio id="bg-music" autoplay loop>
            <source src="data:audio/mp3;base64,{get_audio_base64(audio_path)}" type="audio/mp3">
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

# Function to stop music
def stop_music():
    st.session_state.is_playing = False
    st.markdown(
        """
        <script>
        var audio = document.getElementById("bg-music");
        if (audio) {
            audio.pause();
            audio.currentTime = 0;
        }
        </script>
        """,
        unsafe_allow_html=True,
    )

# Music Control Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("🎵 Play Music"):
        play_music()

with col2:
    if st.button("⏹️ Stop Music"):
        stop_music()

# Persist music state
if st.session_state.is_playing:
    play_music()

st.title("Bi-weekly Work Tracker")

# Job data storage in session_state
if "work_data" not in st.session_state:
    st.session_state.work_data = []

# Graph data storage in session_state with persistent storage
if "graph_data" not in st.session_state:
    st.session_state.graph_data = load_graph_data()

# Layout: Two Columns for Job 1 & Job 2
col1, col2 = st.columns(2)

with col1:
    st.subheader("Pier 50")
    job1_hours = st.text_input("Hours Worked", "", key="job1_hours")
    job1_rate = st.text_input("Hourly Rate ($)", "", key="job1_rate")
    job1_cash_tips = st.text_input("Cash Tips ($)", "", key="job1_cash_tips")
    job1_card_tips = st.text_input("Card Tips ($)", "", key="job1_card_tips")

    if st.button("Add/Update Pier 50 Entry"):
        try:
            job1_hours = float(job1_hours) if job1_hours else 0.0
            job1_rate = float(job1_rate) if job1_rate else 0.0
            job1_cash_tips = float(job1_cash_tips) if job1_cash_tips else 0.0
            job1_card_tips = float(job1_card_tips) if job1_card_tips else 0.0
            add_or_update_entry("Pier 50", job1_hours, job1_rate, job1_cash_tips, job1_card_tips)
        except ValueError:
            st.error("Please enter valid numbers.")

with col2:
    st.subheader("Burgers and Brew")
    job2_hours = st.text_input("Hours Worked", "", key="job2_hours")
    job2_rate = st.text_input("Hourly Rate ($)", "", key="job2_rate")
    job2_card_tips = st.text_input("Card Tips ($)", "", key="job2_card_tips")

    if st.button("Add/Update Burgers and Brew Entry"):
        try:
            job2_hours = float(job2_hours) if job2_hours else 0.0
            job2_rate = float(job2_rate) if job2_rate else 0.0
            job2_card_tips = float(job2_card_tips) if job2_card_tips else 0.0
            add_or_update_entry("Burgers and Brew", job2_hours, job2_rate, 0, job2_card_tips)
        except ValueError:
            st.error("Please enter valid numbers.")

df = pd.DataFrame(st.session_state.work_data)

if not df.empty:
    df.index = df.index + 1
    st.subheader("Work Summary")
    st.dataframe(df)

st.markdown("---")
st.subheader("Earnings Graph Input")

graph_col1, graph_col2 = st.columns(2)

with graph_col1:
    st.subheader("Pier 50 Graph")
    pier50_date = st.text_input("Enter Date (YYYY/MM/DD)", key="pier50_graph_date")
    pier50_earnings = st.text_input("Enter Earnings ($)", key="pier50_graph_earnings")

    if st.button("Add Pier 50"):
        try:
            date_str = pier50_date.replace("/", "-")  # Replace / with -
            date = datetime.strptime(date_str, "%Y-%m-%d").date()  # Parse with dashes
            earnings = float(pier50_earnings) if pier50_earnings else 0.0
            st.session_state.graph_data.append({
                "Date": date,
                "Job Type": "Pier 50",
                "Total Earnings": earnings
            })
            save_graph_data(st.session_state.graph_data)
        except ValueError:
            st.error("Please enter a valid date and earnings amount.")

with graph_col2:
    st.subheader("Burgers and Brew Graph")
    burgers_date = st.text_input("Enter Date (YYYY/MM/DD)", key="burgers_graph_date")
    burgers_earnings = st.text_input("Enter Earnings ($)", key="burgers_graph_earnings")

    if st.button("Add Burgers and Brew"):
        try:
            date_str = burgers_date.replace("/", "-")  # Replace / with -
            date = datetime.strptime(date_str, "%Y-%m-%d").date()  # Parse with dashes
            earnings = float(burgers_earnings) if burgers_earnings else 0.0
            st.session_state.graph_data.append({
                "Date": date,
                "Job Type": "Burgers and Brew",
                "Total Earnings": earnings
            })
            save_graph_data(st.session_state.graph_data)
        except ValueError:
            st.error("Please enter a valid date and earnings amount.")

if st.session_state.graph_data:
    graph_df = pd.DataFrame(st.session_state.graph_data)
    graph_df = graph_df.sort_values('Date')
    fig = px.line(graph_df, x='Date', y='Total Earnings', color='Job Type',
                  title='Daily Earnings by Job', labels={'Total Earnings': 'Earnings ($)', 'Date': 'Work Date'},
                  markers=True)
    fig.update_layout(xaxis_title="Date", yaxis_title="Earnings ($)", legend_title="Job", hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)

    if st.button("Clear Graph Data"):
        if os.path.exists('graph_data.csv'):
            os.remove('graph_data.csv')
        st.session_state.graph_data = []
        st.rerun()
