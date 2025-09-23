"""
Streamlit page for analyzing player performance in penalties.
"""
import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data, get_player_status_counts_over_time, calculate_player_scores, Constants
from typing import List
from datetime import date

st.set_page_config(
    page_title="NFT Weingarten - Player Performance",
    page_icon=Constants.LOGO_PATH,
)

st.title("Player Performance Analysis")
st.markdown(
        """
        This page allows you to compare the performance of multiple players over time,
        visualizing their goals, saves, and shots out.
        """
    )
data: pd.DataFrame = load_data()
data[Constants.DATE_COL] = pd.to_datetime(data[Constants.DATE_COL]).dt.date

st.subheader("Player Score Leaderboard")
st.markdown("This leaderboard ranks players based on a scoring system that assigns points for each shot outcome.")

# Scoring system explanation
scoring_data = {
    'Outcome': ['Goal', 'Saved', 'Out'],
    'Points': [Constants.GOAL_SCORE, Constants.SAVED_SCORE, Constants.OUT_SCORE]
}
scoring_df = pd.DataFrame(scoring_data)
st.dataframe(scoring_df, hide_index=True)

num_months_filter: int = st.slider("Filter for recent N months", 1, 12, 12)
top_players: pd.DataFrame = calculate_player_scores(data, num_months=num_months_filter).head(Constants.TOP_N_PLAYERS_LEADERBOARD)
fig_top_players = px.bar(top_players, x=top_players.index, y=Constants.SCORE_COL,
                         title=f"Top {Constants.TOP_N_PLAYERS_LEADERBOARD} Players by Score (Recent {num_months_filter} Months)",
                         hover_data=[Constants.GOAL_STATUS, Constants.SAVED_STATUS, Constants.OUT_STATUS])
fig_top_players.update_layout(yaxis_title="Score", xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True))
fig_top_players.update_traces(texttemplate='%{y}', textposition='outside')
st.plotly_chart(fig_top_players, config={'displayModeBar': False})
st.dataframe(top_players)

st.subheader("Compare Player Performance Over Time")
player_names: List[str] = list(sorted(data[Constants.SHOOTER_NAME_COL].unique()))
selected_players: List[str] = st.multiselect(
    f"Select up to {Constants.MAX_PLAYER_SELECTIONS} Players to Compare",
    player_names,
    default=player_names[:Constants.DEFAULT_NUM_PLAYERS_MULTISELECT],
    max_selections=Constants.MAX_PLAYER_SELECTIONS,
)

# Generate unique months for the dropdown
data[Constants.MONTH_COL] = pd.to_datetime(data[Constants.DATE_COL]).dt.to_period('M')
unique_months_period: List[pd.Period] = sorted(data[Constants.MONTH_COL].unique(), reverse=True)
unique_months_display: List[str] = [month.strftime("%B %Y") for month in unique_months_period]

selected_month_display: str = st.selectbox("Select a Month", unique_months_display)

# Determine start and end dates for the selected month
if selected_month_display:
    # Convert display format back to Period for date calculation
    selected_month_period: pd.Period = pd.Period(selected_month_display.replace(" ", "-"), freq='M')
    year: int = selected_month_period.year
    month: int = selected_month_period.month
    start_date_filter: date = pd.Timestamp(year=year, month=month, day=1).date()
    end_date_filter: date = (pd.Timestamp(year=year, month=month, day=1) + pd.DateOffset(months=1) - pd.Timedelta(days=1)).date()

    if selected_players:
        st.subheader("Performance Over Time")

        player_status_data: pd.DataFrame = get_player_status_counts_over_time(data, selected_players, start_date=start_date_filter, end_date=end_date_filter)

        if not player_status_data.empty:
            # Aggregate data by player and status for the entire month
            monthly_player_status_summary: pd.DataFrame = player_status_data.groupby([Constants.SHOOTER_NAME_COL, Constants.STATUS_COL])[Constants.COUNT_COL].sum().unstack(fill_value=0).reset_index()

            # Calculate total shots for each player in the month
            monthly_player_status_summary[Constants.TOTAL_SHOTS_COL] = monthly_player_status_summary[Constants.GOAL_STATUS] + monthly_player_status_summary[Constants.SAVED_STATUS] + monthly_player_status_summary[Constants.OUT_STATUS]

            # Calculate score for each player
            monthly_player_status_summary[Constants.SCORE_COL] = (monthly_player_status_summary[Constants.GOAL_STATUS] * Constants.GOAL_SCORE) + (monthly_player_status_summary[Constants.SAVED_STATUS] * Constants.SAVED_SCORE) + (monthly_player_status_summary[Constants.OUT_STATUS] * Constants.OUT_SCORE)

            if not monthly_player_status_summary.empty:
                score_tab, goal_tab, saved_tab, out_tab = st.tabs(["Score", "Goals", "Saved", "Out"])
                with score_tab:
                    fig_total_outcome = px.bar(monthly_player_status_summary, x=Constants.SHOOTER_NAME_COL, y=Constants.SCORE_COL,
                                               title=f"Player Scores in {selected_month_display}",
                                               hover_data=[Constants.GOAL_STATUS, Constants.SAVED_STATUS, Constants.OUT_STATUS, Constants.TOTAL_SHOTS_COL])
                    fig_total_outcome.update_layout(yaxis_title="Score", xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True))
                    st.plotly_chart(fig_total_outcome, use_container_width=True, config={'displayModeBar': False})

                with goal_tab:
                    fig_goals = px.bar(monthly_player_status_summary, x=Constants.SHOOTER_NAME_COL, y=Constants.GOAL_STATUS,
                                       title=f"Goals in {selected_month_display}")
                    fig_goals.update_layout(yaxis_title="Goals", xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True))
                    st.plotly_chart(fig_goals, use_container_width=True, config={'displayModeBar': False})

                with saved_tab:
                    fig_saved = px.bar(monthly_player_status_summary, x=Constants.SHOOTER_NAME_COL, y=Constants.SAVED_STATUS,
                                       title=f"Saved Shots in {selected_month_display}")
                    fig_saved.update_layout(yaxis_title="Saved", xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True))
                    st.plotly_chart(fig_saved, use_container_width=True, config={'displayModeBar': False})

                with out_tab:
                    fig_out = px.bar(monthly_player_status_summary, x=Constants.SHOOTER_NAME_COL, y=Constants.OUT_STATUS,
                                     title=f"Out Shots in {selected_month_display}")
                    fig_out.update_layout(yaxis_title="Out", xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True))
                    st.plotly_chart(fig_out, use_container_width=True, config={'displayModeBar': False})
            else:
                st.info(f"No total outcome data to display for {', '.join(selected_players)} in {selected_month_display}.")