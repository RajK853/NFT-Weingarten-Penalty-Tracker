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
    page_icon="⚽",
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

min_date_leaderboard = data[Constants.DATE_COL].min()
max_date_leaderboard = data[Constants.DATE_COL].max()

selected_date_range = st.date_input(
    "Select date range for Leaderboard",
    value=[min_date_leaderboard, max_date_leaderboard],
    min_value=min_date_leaderboard,
    max_value=max_date_leaderboard
)

leaderboard_start_date = None
leaderboard_end_date = None

if len(selected_date_range) == 2:
    leaderboard_start_date = selected_date_range[0]
    leaderboard_end_date = selected_date_range[1]
elif len(selected_date_range) == 1:
    leaderboard_start_date = selected_date_range[0]
    # If only one date is selected, assume it's the start date and set end date to the same for a single-day range
    leaderboard_end_date = selected_date_range[0]

if leaderboard_start_date and leaderboard_end_date:
    top_players: pd.DataFrame = calculate_player_scores(data, start_date=leaderboard_start_date, end_date=leaderboard_end_date).head(Constants.TOP_N_PLAYERS_LEADERBOARD)
    fig_top_players = px.bar(top_players, x=top_players.index, y=Constants.SCORE_COL,
                             title=f"Top {Constants.TOP_N_PLAYERS_LEADERBOARD} Players by Score",
                             hover_data=[Constants.GOAL_STATUS, Constants.SAVED_STATUS, Constants.OUT_STATUS])
    fig_top_players.update_layout(yaxis_title="Score", xaxis=dict(fixedrange=True), yaxis=dict(range=[0, top_players[Constants.SCORE_COL].max() * 1.1]))
    fig_top_players.update_traces(texttemplate='%{y}', textposition='outside')
    st.plotly_chart(fig_top_players, config={'displayModeBar': False})
    st.dataframe(top_players)
else:
    st.info("Please select both a start and end date for the leaderboard.")

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
        player_status_data[Constants.MONTH_COL] = pd.to_datetime(player_status_data[Constants.DATE_COL]).dt.to_period('M').astype(str)

        if not player_status_data.empty:
            # Aggregate data by player and status for the entire month
            monthly_player_status_summary: pd.DataFrame = player_status_data.groupby([Constants.MONTH_COL, Constants.SHOOTER_NAME_COL, Constants.STATUS_COL])[Constants.COUNT_COL].sum().unstack(fill_value=0).reset_index()

            # Calculate total shots for each player in the month
            monthly_player_status_summary[Constants.TOTAL_SHOTS_COL] = monthly_player_status_summary[Constants.GOAL_STATUS] + monthly_player_status_summary[Constants.SAVED_STATUS] + monthly_player_status_summary[Constants.OUT_STATUS]

            # Calculate score for each player
            monthly_player_status_summary[Constants.SCORE_COL] = (monthly_player_status_summary[Constants.GOAL_STATUS] * Constants.GOAL_SCORE) + (monthly_player_status_summary[Constants.SAVED_STATUS] * Constants.SAVED_SCORE) + (monthly_player_status_summary[Constants.OUT_STATUS] * Constants.OUT_SCORE)

            if not monthly_player_status_summary.empty:
                score_tab, goal_tab, saved_tab, out_tab = st.tabs(["Score", "Goals", "Saved", "Out"])
                with score_tab:
                    max_score = monthly_player_status_summary[Constants.SCORE_COL].max()
                    min_score = monthly_player_status_summary[Constants.SCORE_COL].min()
                    colors_score = ['green' if score == max_score else 'red' if score == min_score else 'lightgray' for score in monthly_player_status_summary[Constants.SCORE_COL]]
                    fig_score_monthly = px.bar(monthly_player_status_summary, x=Constants.SHOOTER_NAME_COL, y=Constants.SCORE_COL,
                                              title="Player Monthly Score")
                    fig_score_monthly.update_traces(marker_color=colors_score)
                    fig_score_monthly.update_layout(yaxis_title="Score", xaxis_title="Player Name", xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True))
                    st.plotly_chart(fig_score_monthly, use_container_width=True, config={'displayModeBar': False})

                with goal_tab:
                    max_goals = monthly_player_status_summary[Constants.GOAL_STATUS].max()
                    min_goals = monthly_player_status_summary[Constants.GOAL_STATUS].min()
                    colors_goals = ['green' if goals == max_goals else 'red' if goals == min_goals else 'lightgray' for goals in monthly_player_status_summary[Constants.GOAL_STATUS]]
                    fig_goals_monthly = px.bar(monthly_player_status_summary, x=Constants.SHOOTER_NAME_COL, y=Constants.GOAL_STATUS,
                                              title="Player Monthly Goals")
                    fig_goals_monthly.update_traces(marker_color=colors_goals)
                    fig_goals_monthly.update_layout(yaxis_title="Goals", xaxis_title="Player Name", xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True))
                    st.plotly_chart(fig_goals_monthly, use_container_width=True, config={'displayModeBar': False})

                with saved_tab:
                    max_saved = monthly_player_status_summary[Constants.SAVED_STATUS].max()
                    min_saved = monthly_player_status_summary[Constants.SAVED_STATUS].min()
                    colors_saved = ['green' if saved == max_saved else 'red' if saved == min_saved else 'lightgray' for saved in monthly_player_status_summary[Constants.SAVED_STATUS]]
                    fig_saved_monthly = px.bar(monthly_player_status_summary, x=Constants.SHOOTER_NAME_COL, y=Constants.SAVED_STATUS,
                                              title="Player Monthly Saved Shots")
                    fig_saved_monthly.update_traces(marker_color=colors_saved)
                    fig_saved_monthly.update_layout(yaxis_title="Saved Shots", xaxis_title="Player Name", xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True))
                    st.plotly_chart(fig_saved_monthly, use_container_width=True, config={'displayModeBar': False})

                with out_tab:
                    max_out = monthly_player_status_summary[Constants.OUT_STATUS].max()
                    min_out = monthly_player_status_summary[Constants.OUT_STATUS].min()
                    colors_out = ['red' if out_val == max_out else 'green' if out_val == min_out else 'lightgray' for out_val in monthly_player_status_summary[Constants.OUT_STATUS]]
                    fig_out_monthly = px.bar(monthly_player_status_summary, x=Constants.SHOOTER_NAME_COL, y=Constants.OUT_STATUS,
                                            title="Player Monthly Out Shots")
                    fig_out_monthly.update_traces(marker_color=colors_out)
                    fig_out_monthly.update_layout(yaxis_title="Out Shots", xaxis_title="Player Name", xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True))
                    st.plotly_chart(fig_out_monthly, use_container_width=True, config={'displayModeBar': False})


            else:
                st.info(f"No data available for the selected players in {selected_month_display}. Please select different players or a different month. 😔")