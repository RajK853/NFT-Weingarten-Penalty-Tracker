import streamlit as st
from src import ui

ui.setup_page(
    page_title="NFT Weingarten Penalty Tracker",
    page_icon="⚽",
    page_description="",
    render_logo=False,
)

st.markdown("""
<style>
.stPageLink {
    background-color: rgba(255, 255, 255, 0.1); /* Slightly visible background */
    padding: 15px 20px;
    border-radius: 10px;
    text-align: center;
    font-size: 1.3em; /* Larger font size */
    font-weight: bold;
    color: #ADD8E6; /* Light blue color for text */
    text-decoration: none; /* Remove underline */
    display: flex; /* Use flexbox for centering content */
    justify-content: center; /* Center content horizontally */
    align-items: center; /* Center content vertically */
    width: 220px; /* Fixed width for all links */
    height: 80px; /* Fixed height for all links */
    margin: 0 auto; /* Center the page link */
    margin-bottom: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Subtle shadow */
    transition: all 0.3s ease-in-out; /* Smooth transition for hover effects */
}

.stPageLink:hover {
    background-color: rgba(255, 255, 255, 0.2); /* Darker background on hover */
    color: #FFFFFF; /* White text on hover */
    transform: translateY(-3px); /* Slight lift effect */
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3); /* Enhanced shadow on hover */
}

/* Adjust icon size if necessary, though Streamlit handles icons well */
.stPageLink > svg {
    font-size: 1.5em; /* Example: make icon slightly larger */
    vertical-align: middle;
    margin-right: 10px;
}
</style>
""", unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1, 4, 1])
with col_center:
    st.image('data/nft_image.jpg', width="stretch")

# First row of links
col1_1, col1_2, col1_3, col1_4, col1_5, col1_6 = st.columns([1, 1, 1, 1, 1, 1])

with col1_2:
    st.page_link("pages/1_Dashboard.py", label="Dashboard", icon="📊")

with col1_3:
    st.page_link("pages/2_Goalkeeper_Analysis.py", label="Goalkeeper Analysis", icon="🧤")

with col1_4:
    st.page_link("pages/1_Player_Performance.py", label="Player Performance", icon="⚽")
    
with col1_5:
    st.page_link("pages/3_Scoring_Method.py", label="Scoring Method", icon="ℹ️")
