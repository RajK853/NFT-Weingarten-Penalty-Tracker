"""
Streamlit page for analyzing shot distribution in penalty shootouts.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils import load_data, get_goal_post_distribution_percentages, create_goal_post_visualization, Constants
from typing import List, Optional

st.set_page_config(
    page_title="NFT Weingarten - Shot Distribution",
)

st.title("Shot Distribution Analysis")
st.markdown(
        """
        This page visualizes the effectiveness of different shoot positions and the individual goal distribution of players.
        """
    )

data: pd.DataFrame = load_data()

st.subheader("Overall Shoot Position Effectiveness")
num_months_filter_position: int = st.slider("Filter for recent N months for Shoot Position Effectiveness", 
                                            Constants.SLIDER_MIN_MONTHS, Constants.SLIDER_MAX_MONTHS, Constants.SLIDER_DEFAULT_MONTHS, 
                                            key="shoot_position_months")
grid_percentages: dict = get_goal_post_distribution_percentages(data, player_name=None, num_months=num_months_filter_position)
st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})

st.subheader("Individual Player Goal Distribution")
st.markdown(
        """
        Explore the goal distribution of individual players based on their shoot positions.
        Select a player from the sidebar to see where they tend to aim their shots.
        """
    )
st.sidebar.header("Individual Player Analysis")

individual_player_names: List[str]
selected_individual_player: Optional[str]

if data.empty:
    st.warning("No data available to display player distribution.")
    individual_player_names = []
    selected_individual_player = None
else:
    individual_player_names = list(data[Constants.SHOOTER_NAME_COL].unique())
    selected_individual_player = st.sidebar.selectbox("Select a Player for Goal Distribution", individual_player_names, key="individual_player_selection")

if selected_individual_player:
    st.subheader(f"{selected_individual_player}'s Goal Distribution by Shoot Position")
    
    grid_percentages: dict = get_goal_post_distribution_percentages(data, selected_individual_player, decimal_points=Constants.DECIMAL_POINTS_DISPLAY)
    fig = create_goal_post_visualization(grid_percentages)
    st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})