import streamlit as st
import plotly.express as px
from utils import load_data, get_shoot_position_goals, Constants

st.title("Individual Player Goal Distribution")
st.markdown(
        """
        Explore the goal distribution of individual players based on their shoot positions.
        Select a player from the sidebar to see where they tend to aim their shots.
        """
    )
st.sidebar.header("Individual Player Analysis")
data = load_data()
individual_player_names = data[Constants.SHOOTER_NAME_COL].unique()
selected_individual_player = st.sidebar.selectbox("Select a Player for Goal Distribution", individual_player_names)

if selected_individual_player:
    st.subheader(f"{selected_individual_player}'s Goal Distribution by Shoot Position")
    shoot_position_goals = get_shoot_position_goals(data, selected_individual_player)
    fig_positions = px.bar(shoot_position_goals, x=Constants.SHOOT_POSITION_COL, y=Constants.COUNT_COL, title=f"{selected_individual_player}'s Goal Distribution by Shoot Position")
    st.plotly_chart(fig_positions)
