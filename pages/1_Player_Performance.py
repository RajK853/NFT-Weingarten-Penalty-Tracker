"""
Streamlit page for analyzing player performance in penalties.
"""
import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data, get_player_status_counts_over_time, calculate_player_scores, Constants, _get_date_range_from_month_display
from typing import List
from datetime import date

st.set_page_config(
    page_title="NFT Weingarten - Player Performance",
    page_icon=Constants.EMOJI_PLAYER_PAGE,
)

st.title("Player Performance Analysis")
st.markdown(
        """
        This page is dedicated to in-depth analysis of individual player performance in penalty shootouts. 
        Utilize the interactive tools below to compare players, understand their scoring consistency, 
        and identify top performers based on various metrics over customizable timeframes.
        """
    )
data: pd.DataFrame = load_data()
data[Constants.DATE_COL] = pd.to_datetime(data[Constants.DATE_COL]).dt.date

st.subheader("Player Score Leaderboard")
st.markdown("This leaderboard ranks players based on a comprehensive scoring system that assigns points for each shot outcome (Goal, Saved, Out). A higher score indicates superior overall performance in penalty shootouts. Use the date range selector to analyze performance during specific periods.")

# Scoring system explanation
scoring_data = {
    'Outcome': [Constants.TAB_GOALS, Constants.TAB_SAVED, Constants.TAB_OUT],
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
    min_score_val = top_players[Constants.SCORE_COL].min()
    max_score_val = top_players[Constants.SCORE_COL].max()
    buffer = (max_score_val - min_score_val) * Constants.CHART_Y_AXIS_BUFFER # 10% buffer
    y_range_min = min_score_val - buffer
    y_range_max = max_score_val + buffer
    fig_top_players.update_layout(yaxis_title="Score", xaxis=dict(fixedrange=Constants.PLOTLY_FIXED_RANGE), yaxis=dict(range=[y_range_min, y_range_max]))
    fig_top_players.update_traces(texttemplate=Constants.PLOTLY_TEXT_TEMPLATE, textposition=Constants.PLOTLY_TEXT_POSITION_OUTSIDE)
    st.plotly_chart(fig_top_players, config={'displayModeBar': Constants.PLOTLY_DISPLAY_MODE_BAR})
    st.dataframe(top_players)
else:
    st.info(Constants.INFO_SELECT_DATE_RANGE)

st.subheader("Compare Player Performance Over Time")
st.markdown("Select multiple players and a specific month to analyze their aggregated performance across different outcome categories (Score, Goals, Saved, Out). This section provides a detailed breakdown of how selected players performed within the chosen timeframe.")
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
    start_date_filter, end_date_filter = _get_date_range_from_month_display(selected_month_display)

    if selected_players:
        st.subheader("Performance Over Time")

        player_status_data: pd.DataFrame = get_player_status_counts_over_time(data, selected_players, start_date=start_date_filter, end_date=end_date_filter)
        player_status_data[Constants.MONTH_COL] = pd.to_datetime(player_status_data[Constants.DATE_COL]).dt.to_period('M').astype(str)

        if not player_status_data.empty:
            # Aggregate data by player and status for the entire month
            monthly_player_status_summary: pd.DataFrame = player_status_data.groupby([Constants.MONTH_COL, Constants.SHOOTER_NAME_COL, Constants.STATUS_COL])[Constants.COUNT_COL].sum().unstack(fill_value=Constants.DEFAULT_FILL_VALUE).reset_index()

            # Calculate total shots for each player in the month
            monthly_player_status_summary[Constants.TOTAL_SHOTS_COL] = monthly_player_status_summary[Constants.GOAL_STATUS] + monthly_player_status_summary[Constants.SAVED_STATUS] + monthly_player_status_summary[Constants.OUT_STATUS]

            # Calculate score for each player
            monthly_player_status_summary[Constants.SCORE_COL] = (monthly_player_status_summary[Constants.GOAL_STATUS] * Constants.GOAL_SCORE) + (monthly_player_status_summary[Constants.SAVED_STATUS] * Constants.SAVED_SCORE) + (monthly_player_status_summary[Constants.OUT_STATUS] * Constants.OUT_SCORE)

            if not monthly_player_status_summary.empty:
                score_tab, goal_tab, saved_tab, out_tab = st.tabs([Constants.TAB_SCORE, Constants.TAB_GOALS, Constants.TAB_SAVED, Constants.TAB_OUT])
                with score_tab:
                    max_score = monthly_player_status_summary[Constants.SCORE_COL].max()
                    min_score = monthly_player_status_summary[Constants.SCORE_COL].min()
                    colors_score = [Constants.COLOR_GREEN if score == max_score else Constants.COLOR_RED if score == min_score else Constants.COLOR_LIGHTGRAY for score in monthly_player_status_summary[Constants.SCORE_COL]]
                    fig_score_monthly = px.bar(monthly_player_status_summary, x=Constants.SHOOTER_NAME_COL, y=Constants.SCORE_COL,
                                              title="Player Monthly Score")
                    fig_score_monthly.update_traces(marker_color=colors_score)
                    fig_score_monthly.update_layout(yaxis_title="Score", xaxis_title="Player Name", xaxis=dict(fixedrange=Constants.PLOTLY_FIXED_RANGE), yaxis=dict(fixedrange=Constants.PLOTLY_FIXED_RANGE))
                    st.plotly_chart(fig_score_monthly, use_container_width=True, config={'displayModeBar': Constants.PLOTLY_DISPLAY_MODE_BAR})

                with goal_tab:
                    max_goals = monthly_player_status_summary[Constants.GOAL_STATUS].max()
                    min_goals = monthly_player_status_summary[Constants.GOAL_STATUS].min()
                    colors_goals = [Constants.COLOR_GREEN if goals == max_goals else Constants.COLOR_RED if goals == min_goals else Constants.COLOR_LIGHTGRAY for goals in monthly_player_status_summary[Constants.GOAL_STATUS]]
                    fig_goals_monthly = px.bar(monthly_player_status_summary, x=Constants.SHOOTER_NAME_COL, y=Constants.GOAL_STATUS,
                                              title="Player Monthly Goals")
                    fig_goals_monthly.update_traces(marker_color=colors_goals)
                    fig_goals_monthly.update_layout(yaxis_title="Goals", xaxis_title="Player Name", xaxis=dict(fixedrange=Constants.PLOTLY_FIXED_RANGE), yaxis=dict(fixedrange=Constants.PLOTLY_FIXED_RANGE))
                    st.plotly_chart(fig_goals_monthly, use_container_width=True, config={'displayModeBar': Constants.PLOTLY_DISPLAY_MODE_BAR})

                with saved_tab:
                    max_saved = monthly_player_status_summary[Constants.SAVED_STATUS].max()
                    min_saved = monthly_player_status_summary[Constants.SAVED_STATUS].min()
                    colors_saved = [Constants.COLOR_GREEN if saved == max_saved else Constants.COLOR_RED if saved == min_saved else Constants.COLOR_LIGHTGRAY for saved in monthly_player_status_summary[Constants.SAVED_STATUS]]
                    fig_saved_monthly = px.bar(monthly_player_status_summary, x=Constants.SHOOTER_NAME_COL, y=Constants.SAVED_STATUS,
                                              title="Player Monthly Saved Shots")
                    fig_saved_monthly.update_traces(marker_color=colors_saved)
                    fig_saved_monthly.update_layout(yaxis_title="Saved Shots", xaxis_title="Player Name", xaxis=dict(fixedrange=Constants.PLOTLY_FIXED_RANGE), yaxis=dict(fixedrange=Constants.PLOTLY_FIXED_RANGE))
                    st.plotly_chart(fig_saved_monthly, use_container_width=True, config={'displayModeBar': Constants.PLOTLY_DISPLAY_MODE_BAR})

                with out_tab:
                    max_out = monthly_player_status_summary[Constants.OUT_STATUS].max()
                    min_out = monthly_player_status_summary[Constants.OUT_STATUS].min()
                    colors_out = [Constants.COLOR_RED if out_val == max_out else Constants.COLOR_GREEN if out_val == min_out else Constants.COLOR_LIGHTGRAY for out_val in monthly_player_status_summary[Constants.OUT_STATUS]]
                    fig_out_monthly = px.bar(monthly_player_status_summary, x=Constants.SHOOTER_NAME_COL, y=Constants.OUT_STATUS,
                                            title="Player Monthly Out Shots")
                    fig_out_monthly.update_traces(marker_color=colors_out)
                    fig_out_monthly.update_layout(yaxis_title="Out Shots", xaxis_title="Player Name", xaxis=dict(fixedrange=Constants.PLOTLY_FIXED_RANGE), yaxis=dict(fixedrange=Constants.PLOTLY_FIXED_RANGE))
                    st.plotly_chart(fig_out_monthly, use_container_width=True, config={'displayModeBar': Constants.PLOTLY_DISPLAY_MODE_BAR})


            else:
                st.info(Constants.INFO_NO_PLAYER_DATA.format(selected_month_display=selected_month_display))