import streamlit as st
import plotly.express as px
from utils import load_data, calculate_goal_percentage, Constants

st.set_page_config(
    page_title="NFT Weingarten - Penalty Tracker",
)

col1, col2 = st.columns([1, 4])
with col1:
    st.image(Constants.LOGO_PATH, width=100)
with col2:
    st.title("Penalty Shootout Dashboard")

st.markdown(
        """
        This interactive dashboard visualizes penalty shootout data, offering insights into player performance and shot outcomes.
        Explore key statistics and trends from various penalty shootouts.
        """
    )

st.subheader("Top 10 Players by Goal Percentage")
data = load_data()
top_10_players = calculate_goal_percentage(data).head(10)
fig_top_players = px.bar(top_10_players, x=top_10_players.index, y=Constants.GOAL_PERCENTAGE_COL, title="Top 10 Players by Goal Percentage")
st.plotly_chart(fig_top_players)
