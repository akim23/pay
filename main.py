import streamlit as st
import pandas as pd
import base64

# Function to encode an image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

# Path to your local image
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

# Streamlit UI setup
st.title("Weekly Work Tracker")

# Job data storage in session_state
if "work_data" not in st.session_state:
    st.session_state.work_data = []

# Function to add or update job entry
def add_or_update_entry(job_type, hours, rate, cash_tips, card_tips):
    total_tips = cash_tips + card_tips
    hourly_tips = total_tips / hours if hours > 0 else 0
    hourly_earnings = (hours * rate + total_tips) / hours if hours > 0 else 0  # Hourly earnings including tips
    total_pay = (hours * rate) + total_tips

    # Check if the job entry exists already, update it, otherwise add new entry
    updated = False
    for i, entry in enumerate(st.session_state.work_data):
        if entry['Job Type'] == job_type:
            st.session_state.work_data[i] = {
                "Job Type": job_type, "Hours Worked": hours, "Hourly Rate": rate,
                "Cash Tips": cash_tips, "Card Tips": card_tips, "Total Tips": total_tips,
                "Hourly Tips": hourly_tips, "Hourly Earnings": hourly_earnings, "Total Earnings": total_pay
            }
            updated = True
            break

    # If job entry doesn't exist, add new one
    if not updated:
        st.session_state.work_data.append({
            "Job Type": job_type, "Hours Worked": hours, "Hourly Rate": rate,
            "Cash Tips": cash_tips, "Card Tips": card_tips, "Total Tips": total_tips,
            "Hourly Tips": hourly_tips, "Hourly Earnings": hourly_earnings, "Total Earnings": total_pay
        })

# Layout: Two Columns for Job 1 & Job 2
col1, col2 = st.columns(2)

with col1:
    st.subheader("Job 1")

    # Input fields for Job 1
    job1_hours = st.text_input("Hours Worked (Job 1)", "", key="job1_hours")
    job1_rate = st.text_input("Hourly Rate ($) (Job 1)", "", key="job1_rate")
    job1_cash_tips = st.text_input("Cash Tips ($) (Job 1)", "", key="job1_cash_tips")
    job1_card_tips = st.text_input("Card Tips ($) (Job 1)", "", key="job1_card_tips")

    # Button to add or update Job 1 entry
    if st.button("Add/Update Job 1 Entry"):
        try:
            job1_hours = float(job1_hours) if job1_hours else 0.0
            job1_rate = float(job1_rate) if job1_rate else 0.0
            job1_cash_tips = float(job1_cash_tips) if job1_cash_tips else 0.0
            job1_card_tips = float(job1_card_tips) if job1_card_tips else 0.0
            add_or_update_entry("Job 1", job1_hours, job1_rate, job1_cash_tips, job1_card_tips)
        except ValueError:
            st.error("Please enter valid numbers for all fields.")

with col2:
    st.subheader("Job 2")

    # Input fields for Job 2
    job2_hours = st.text_input("Hours Worked (Job 2)", "", key="job2_hours")
    job2_rate = st.text_input("Hourly Rate ($) (Job 2)", "", key="job2_rate")
    job2_card_tips = st.text_input("Card Tips ($) (Job 2)", "", key="job2_card_tips")

    # Button to add or update Job 2 entry
    if st.button("Add/Update Job 2 Entry"):
        try:
            job2_hours = float(job2_hours) if job2_hours else 0.0
            job2_rate = float(job2_rate) if job2_rate else 0.0
            job2_card_tips = float(job2_card_tips) if job2_card_tips else 0.0
            add_or_update_entry("Job 2", job2_hours, job2_rate, 0, job2_card_tips)  # No cash tips for Job 2
        except ValueError:
            st.error("Please enter valid numbers for all fields.")

# Convert data to DataFrame
df = pd.DataFrame(st.session_state.work_data)

# Adjust the index to start from 1
df.index = df.index + 1

if not df.empty:
    st.subheader("Work Summary")
    st.dataframe(df)

    # Weekly totals per job (Job 1 and Job 2)
    job1_df = df[df["Job Type"] == "Job 1"]
    job2_df = df[df["Job Type"] == "Job 2"]

    weekly_hours_job1 = job1_df["Hours Worked"].sum()
    weekly_hours_job2 = job2_df["Hours Worked"].sum()

    weekly_earnings_job1 = job1_df["Total Earnings"].sum()
    weekly_earnings_job2 = job2_df["Total Earnings"].sum()

    weekly_hourly_earnings_job1 = weekly_earnings_job1 / weekly_hours_job1 if weekly_hours_job1 > 0 else 0
    weekly_hourly_earnings_job2 = weekly_earnings_job2 / weekly_hours_job2 if weekly_hours_job2 > 0 else 0

    # Display weekly earnings in two columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Job 1 Weekly Totals")
        st.write(f"**Total Hours:** {weekly_hours_job1}")
        st.write(f"**Total Earnings:** ${weekly_earnings_job1:.2f}")
        st.write(f"**Avg Hourly Earnings:** ${weekly_hourly_earnings_job1:.2f}")

    with col2:
        st.subheader("Job 2 Weekly Totals")
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

