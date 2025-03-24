import streamlit as st
import pandas as pd
import base64
import plotly.express as px
from datetime import datetime
import os
from functions import add_or_update_entry, load_graph_data, save_graph_data

# Function to encode an image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string


# Path to your local background image
image_path = "images/back1.jpg"  # Change this to the path of your image
encoded_image = image_to_base64(image_path)

# Set background image using base64 encoding
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('data:image/jpeg;base64,{encoded_image}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        height: 100%;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Path to title image
title_image_path = "images/KBC.webp"  # Change this to your .webp image path

# Display title image
st.image(title_image_path, use_container_width=True)

# Streamlit UI setup
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

    # Input fields for Job 1
    job1_hours = st.text_input("Hours Worked", "", key="job1_hours")
    job1_rate = st.text_input("Hourly Rate ($)", "", key="job1_rate")
    job1_cash_tips = st.text_input("Cash Tips ($)", "", key="job1_cash_tips")
    job1_card_tips = st.text_input("Card Tips ($)", "", key="job1_card_tips")

    # Button to add or update Job 1 entry
    if st.button("Add/Update Pier 50 Entry"):
        try:
            job1_hours = float(job1_hours) if job1_hours else 0.0
            job1_rate = float(job1_rate) if job1_rate else 0.0
            job1_cash_tips = float(job1_cash_tips) if job1_cash_tips else 0.0
            job1_card_tips = float(job1_card_tips) if job1_card_tips else 0.0
            add_or_update_entry("Pier 50", job1_hours, job1_rate, job1_cash_tips, job1_card_tips)
        except ValueError:
            st.error("Please enter valid numbers for all fields.")

with col2:
    st.subheader("Burgers and Brew")

    # Input fields for Job 2
    job2_hours = st.text_input("Hours Worked", "", key="job2_hours")
    job2_rate = st.text_input("Hourly Rate ($)", "", key="job2_rate")
    job2_card_tips = st.text_input("Card Tips ($)", "", key="job2_card_tips")

    # Button to add or update Job 2 entry
    if st.button("Add/Update Burgers and Brew Entry"):
        try:
            job2_hours = float(job2_hours) if job2_hours else 0.0
            job2_rate = float(job2_rate) if job2_rate else 0.0
            job2_card_tips = float(job2_card_tips) if job2_card_tips else 0.0
            add_or_update_entry("Burgers and Brew", job2_hours, job2_rate, 0, job2_card_tips)  # No cash tips for Job 2
        except ValueError:
            st.error("Please enter valid numbers for all fields.")

# Convert data to DataFrame
df = pd.DataFrame(st.session_state.work_data)

if not df.empty:
    # Adjust the index to start from 1 for the data table
    df.index = df.index + 1

    st.subheader("Work Summary")
    st.dataframe(df)

    # Weekly totals per job
    pier50_df = df[df["Job Type"] == "Pier 50"]
    burgers_df = df[df["Job Type"] == "Burgers and Brew"]

    weekly_hours_job1 = pier50_df["Hours Worked"].sum()
    weekly_hours_job2 = burgers_df["Hours Worked"].sum()

    weekly_earnings_job1 = pier50_df["Total Earnings"].sum()
    weekly_earnings_job2 = burgers_df["Total Earnings"].sum()

    weekly_hourly_earnings_job1 = weekly_earnings_job1 / weekly_hours_job1 if weekly_hours_job1 > 0 else 0
    weekly_hourly_earnings_job2 = weekly_earnings_job2 / weekly_hours_job2 if weekly_hours_job2 > 0 else 0

    # Display weekly earnings in two columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Pier 50 Weekly Totals")
        st.write(f"**Total Hours:** {weekly_hours_job1}")
        st.write(f"**Total Earnings:** ${weekly_earnings_job1:.2f}")
        st.write(f"**Avg Hourly Earnings:** ${weekly_hourly_earnings_job1:.2f}")

    with col2:
        st.subheader("Burgers and Brew Weekly Totals")
        st.write(f"**Total Hours:** {weekly_hours_job2}")
        st.write(f"**Total Earnings:** ${weekly_earnings_job2:.2f}")
        st.write(f"**Avg Hourly Earnings:** ${weekly_hourly_earnings_job2:.2f}")

    # Button to calculate total earnings for both jobs
    if st.button("Calculate Total Earnings (Both Jobs)"):
        total_weekly_hours = weekly_hours_job1 + weekly_hours_job2
        total_weekly_earnings = weekly_earnings_job1 + weekly_earnings_job2
        total_hourly_earnings = total_weekly_earnings / total_weekly_hours if total_weekly_hours > 0 else 0

        st.subheader("Total Weekly Earnings (Both Jobs)")
        st.write(f"**Total Hours:** {total_weekly_hours}")
        st.write(f"**Total Earnings:** ${total_weekly_earnings:.2f}")
        st.write(f"**Avg Hourly Earnings:** ${total_hourly_earnings:.2f}")

# Separate Graph Input Section
st.markdown("---")  # Add a horizontal line for separation
st.subheader("Earnings Graph Input")

# Create two columns for the graph input
graph_col1, graph_col2 = st.columns(2)

with graph_col1:
    st.subheader("Pier 50 Graph")
    pier50_date = st.text_input("Enter Date (YYYY-MM-DD)", key="pier50_graph_date")
    pier50_earnings = st.text_input("Enter Earnings ($)", key="pier50_graph_earnings")

    if st.button("Add Pier 50"):
        try:
            # Convert string date to datetime
            date = datetime.strptime(pier50_date, "%Y-%m-%d").date()
            earnings = float(pier50_earnings) if pier50_earnings else 0.0

            st.session_state.graph_data.append({
                "Date": date,
                "Job Type": "Pier 50",
                "Total Earnings": earnings
            })
            save_graph_data(st.session_state.graph_data)  # Save after adding new data
        except ValueError:
            st.error("Please enter valid date (YYYY-MM-DD) and earnings amount")

with graph_col2:
    st.subheader("Burgers and Brew Graph")
    burgers_date = st.text_input("Enter Date (YYYY-MM-DD)", key="burgers_graph_date")
    burgers_earnings = st.text_input("Enter Earnings ($)", key="burgers_graph_earnings")

    if st.button("Add Burgers and Brew"):
        try:
            # Convert string date to datetime
            date = datetime.strptime(burgers_date, "%Y-%m-%d").date()
            earnings = float(burgers_earnings) if burgers_earnings else 0.0

            st.session_state.graph_data.append({
                "Date": date,
                "Job Type": "Burgers and Brew",
                "Total Earnings": earnings
            })
            save_graph_data(st.session_state.graph_data)  # Save after adding new data
        except ValueError:
            st.error("Please enter valid date (YYYY-MM-DD) and earnings amount")

# Convert graph data to DataFrame and create the visualization
if st.session_state.graph_data:
    graph_df = pd.DataFrame(st.session_state.graph_data)
    graph_df = graph_df.sort_values('Date')

    # Create line plot using plotly
    fig = px.line(graph_df, x='Date', y='Total Earnings', color='Job Type',
                  title='Daily Earnings by Job',
                  labels={'Total Earnings': 'Earnings ($)', 'Date': 'Work Date'},
                  markers=True)

    # Customize the graph
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Earnings ($)",
        legend_title="Job",
        hovermode='x unified'
    )

    # Display the graph
    st.plotly_chart(fig, use_container_width=True)

    # Add a button to clear graph data
    if st.button("Clear Graph Data"):
        if os.path.exists('graph_data.csv'):
            os.remove('graph_data.csv')
        st.session_state.graph_data = []
        st.rerun()
