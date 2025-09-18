import streamlit as st
import plotly.express as px
from utils import load_data, calculate_goal_miss_ratio, display_header, Constants

st.set_page_config(
    page_title="NFT Weingarten - Penalty Tracker",
)

display_header()

st.subheader("Top 10 Players by Goal-to-Miss Ratio")
data = load_data()
top_10_players = calculate_goal_miss_ratio(data).head(10)
fig_top_players = px.bar(top_10_players, x=top_10_players.index, y=Constants.GOAL_RATIO_COL, title="Top 10 Players by Goal Percentage")
st.plotly_chart(fig_top_players)
