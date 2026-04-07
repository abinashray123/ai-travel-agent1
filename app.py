
# app.py — VERY TOP (before ALL other imports)

import os
from pathlib import Path

# ✅ Point Python to your project-local CA bundle (NO admin needed)
CA_BUNDLE_PATH = Path(__file__).parent / "certs" / "cacert.pem"

os.environ["SSL_CERT_FILE"] = str(CA_BUNDLE_PATH)
os.environ["REQUESTS_CA_BUNDLE"] = str(CA_BUNDLE_PATH)

# --------------------------------------------------

import warnings
warnings.filterwarnings("ignore")

from dotenv import load_dotenv
load_dotenv()  # ✅ after SSL is configured

import streamlit as st
st.write("SSL_CERT_FILE =", os.environ.get("SSL_CERT_FILE"))
from src.core.planner import TravelPlanner
from src.utils.logger import get_logger


logger = get_logger(__name__)


st.set_page_config(page_title="AI Travel Planner", layout="wide")
st.title("🌍 AI Travel Itinerary Planner")

with st.form("planner_form"):
    city = st.text_input("📍 City")
    days = st.slider("🗓️ Number of days", 1, 10, 3)
    interests = st.text_input("🎯 Interests (comma-separated)")
    style = st.selectbox("💰 Travel Style", ["Budget", "Mid-range", "Luxury"])
    pace = st.selectbox("🚶 Pace", ["Relaxed", "Balanced", "Packed"])
    month = st.selectbox("📅 Month (optional)", ["Any"] + [
        "Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"
    ])

    submitted = st.form_submit_button("✨ Generate Itinerary")

if submitted:
    if city and interests:
        planner = TravelPlanner()

        itinerary = planner.create_itinerary(
            city=city,
            days=days,
            interests=[i.strip() for i in interests.split(",")],
            style=style,
            pace=pace,
            month=None if month == "Any" else month
        )

        st.subheader("📄 Your Travel Plan")
        st.markdown(itinerary)
        
        logger.info("RESPONSE GENERATED")
    else:
        st.warning("Please enter city and interests")
