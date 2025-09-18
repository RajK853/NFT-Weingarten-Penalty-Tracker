import streamlit as st
import plotly.express as px
from utils import load_data, get_player_status_counts_over_time, Constants

st.subheader("Compare Player Performance Over Time")
data = load_data()
player_names = data[Constants.SHOOTER_NAME_COL].unique()
selected_players = st.multiselect("Select up to 5 Players to Compare", player_names, default=player_names[:2], max_selections=Constants.MAX_PLAYER_SELECTIONS)

if selected_players:
    st.subheader(f"Performance Over Time")
    player_status_data = get_player_status_counts_over_time(data, selected_players)
    
    if not player_status_data.empty:
        status_colors = {Constants.GOAL_STATUS: "green", Constants.SAVED_STATUS: "orange", Constants.OUT_STATUS: "red"}
        status_titles = {Constants.GOAL_STATUS: "Goals Over Time", Constants.SAVED_STATUS: "Saves Over Time", Constants.OUT_STATUS: "Outs Over Time"}

        for status in status_colors.keys():
            status_df = player_status_data[player_status_data[Constants.STATUS_COL] == status]
            if not status_df.empty:
                fig = px.scatter(status_df,
                              x=Constants.DATE_COL,
                              y=Constants.COUNT_COL,
                              color=Constants.SHOOTER_NAME_COL,
                              size=[Constants.SCATTER_POINT_SIZE]*len(status_df),
                              title=f"{', '.join(selected_players)} - {status_titles[status]}")
                st.plotly_chart(fig)
            else:
                st.info(f"No {status} data to display for selected players.")
    else:
        st.info("No data to display for selected players.")
