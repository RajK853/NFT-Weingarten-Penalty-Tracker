"""
Streamlit page for analyzing player performance in penalties.
"""
import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data, get_player_status_counts_over_time, calculate_player_scores, Constants, _get_date_range_from_month_display, gender_selection_ui
from typing import List
from datetime import date

st.set_page_config(
    page_title="NFT Weingarten - Player Performance",
    page_icon=Constants.UI.EMOJI_PLAYER_PAGE,
    initial_sidebar_state="expanded",
    layout="wide"
)

# --- Header ---

col1, col2, col3 = st.columns([1,0.5,1])
with col2:
    st.image(Constants.Paths.LOGO, use_container_width=True)

st.markdown("<h1 style='text-align: center;'>Player Performance Analysis</h1>", unsafe_allow_html=True)

st.markdown(
    """
    This page is dedicated to in-depth analysis of individual player performance in penalty shootouts. 
    Utilize the interactive tools below to compare players, understand their scoring consistency, 
    and identify top performers based on various metrics over customizable timeframes.
    """
)
st.write("")
st.markdown("---")
gender_selection = gender_selection_ui()
data: pd.DataFrame = load_data(gender=gender_selection)
data[Constants.Columns.DATE] = pd.to_datetime(data[Constants.Columns.DATE]).dt.date

with st.container(border=True):
    st.subheader("Player Score Leaderboard")
    st.markdown("This leaderboard ranks players based on a comprehensive scoring system that assigns points for each shot outcome (Goal, Saved, Out). A higher score indicates superior overall performance in penalty shootouts. Use the date range selector to analyze performance during specific periods.")

    # Scoring system explanation
    scoring_data = {
        'Outcome': [Constants.UI.TAB_GOALS, Constants.UI.TAB_SAVED, Constants.UI.TAB_OUT],
        'Points': [Constants.Scoring.GOAL, Constants.Scoring.SAVED, Constants.Scoring.OUT]
    }
    scoring_df = pd.DataFrame(scoring_data)
    st.dataframe(scoring_df, hide_index=True)

    min_date_leaderboard = data[Constants.Columns.DATE].min()
    max_date_leaderboard = data[Constants.Columns.DATE].max()

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
        top_players: pd.DataFrame = calculate_player_scores(data, start_date=leaderboard_start_date, end_date=leaderboard_end_date).head(Constants.UI.TOP_N_PLAYERS_LEADERBOARD)
        fig_top_players = px.bar(top_players, x=top_players.index, y=Constants.Columns.SCORE,
                                 title=f"Top {Constants.UI.TOP_N_PLAYERS_LEADERBOARD} Players by Score",
                                 hover_data=[Constants.Status.GOAL, Constants.Status.SAVED, Constants.Status.OUT])
        min_score_val = top_players[Constants.Columns.SCORE].min()
        max_score_val = top_players[Constants.Columns.SCORE].max()
        buffer = (max_score_val - min_score_val) * Constants.UI.CHART_Y_AXIS_BUFFER # 10% buffer
        y_range_min = min_score_val - buffer
        y_range_max = max_score_val + buffer
        fig_top_players.update_layout(yaxis_title="Score", xaxis=dict(fixedrange=Constants.UI.PLOTLY_FIXED_RANGE), yaxis=dict(range=[y_range_min, y_range_max]))
        fig_top_players.update_traces(texttemplate=Constants.UI.PLOTLY_TEXT_TEMPLATE, textposition=Constants.UI.PLOTLY_TEXT_POSITION_OUTSIDE)
        st.plotly_chart(fig_top_players, config={'displayModeBar': Constants.UI.PLOTLY_DISPLAY_MODE_BAR})
        st.dataframe(top_players)
    else:
        st.info(Constants.UI.INFO_SELECT_DATE_RANGE)

    st.subheader("Compare Player Performance Over Time")
    st.markdown("Select multiple players and a specific month to analyze their aggregated performance across different outcome categories (Score, Goals, Saved, Out). This section provides a detailed breakdown of how selected players performed within the chosen timeframe.")
    player_names: List[str] = list(sorted(data[Constants.Columns.SHOOTER_NAME].unique()))
    selected_players: List[str] = st.multiselect(
        f"Select up to {Constants.UI.MAX_PLAYER_SELECTIONS} Players to Compare",
        player_names,
        default=player_names[:Constants.UI.DEFAULT_NUM_PLAYERS_MULTISELECT],
        max_selections=Constants.UI.MAX_PLAYER_SELECTIONS,
    )

    # Generate unique months for the dropdown
    data[Constants.Columns.MONTH] = pd.to_datetime(data[Constants.Columns.DATE]).dt.to_period('M')
    unique_months_period: List[pd.Period] = sorted(data[Constants.Columns.MONTH].unique(), reverse=True)
    unique_months_display: List[str] = [month.strftime("%B %Y") for month in unique_months_period]

    selected_month_display: str = st.selectbox("Select a Month", unique_months_display)

    # Determine start and end dates for the selected month
    if selected_month_display:
        start_date_filter, end_date_filter = _get_date_range_from_month_display(selected_month_display)

        if selected_players:
            st.subheader("Performance Over Time")

            player_status_data: pd.DataFrame = get_player_status_counts_over_time(data, selected_players, start_date=start_date_filter, end_date=end_date_filter)
            player_status_data[Constants.Columns.MONTH] = pd.to_datetime(player_status_data[Constants.Columns.DATE]).dt.to_period('M').astype(str)

            if not player_status_data.empty:
                # Aggregate data by player and status for the entire month
                monthly_player_status_summary: pd.DataFrame = player_status_data.groupby([Constants.Columns.MONTH, Constants.Columns.SHOOTER_NAME, Constants.Columns.STATUS])[Constants.Columns.COUNT].sum().unstack(fill_value=Constants.Data.DEFAULT_FILL_VALUE).reset_index()

                # Calculate total shots for each player in the month
                monthly_player_status_summary[Constants.Columns.TOTAL_SHOTS] = monthly_player_status_summary[Constants.Status.GOAL] + monthly_player_status_summary[Constants.Status.SAVED] + monthly_player_status_summary[Constants.Status.OUT]

                # Calculate score for each player
                monthly_player_status_summary[Constants.Columns.SCORE] = (monthly_player_status_summary[Constants.Status.GOAL] * Constants.Scoring.GOAL) + (monthly_player_status_summary[Constants.Status.SAVED] * Constants.Scoring.SAVED) + (monthly_player_status_summary[Constants.Status.OUT] * Constants.Scoring.OUT)

                if not monthly_player_status_summary.empty:
                    score_tab, goal_tab, saved_tab, out_tab = st.tabs([Constants.UI.TAB_SCORE, Constants.UI.TAB_GOALS, Constants.UI.TAB_SAVED, Constants.UI.TAB_OUT])
                    with score_tab:
                        max_score = monthly_player_status_summary[Constants.Columns.SCORE].max()
                        min_score = monthly_player_status_summary[Constants.Columns.SCORE].min()
                        colors_score = [Constants.UI.COLOR_GREEN if score == max_score else Constants.UI.COLOR_RED if score == min_score else Constants.UI.COLOR_LIGHTGRAY for score in monthly_player_status_summary[Constants.Columns.SCORE]]
                        fig_score_monthly = px.bar(monthly_player_status_summary, x=Constants.Columns.SHOOTER_NAME, y=Constants.Columns.SCORE,
                                                  title="Player Monthly Score")
                        fig_score_monthly.update_traces(marker_color=colors_score)
                        fig_score_monthly.update_layout(yaxis_title="Score", xaxis_title="Player Name", xaxis=dict(fixedrange=Constants.UI.PLOTLY_FIXED_RANGE), yaxis=dict(fixedrange=Constants.UI.PLOTLY_FIXED_RANGE))
                        st.plotly_chart(fig_score_monthly, use_container_width=True, config={'displayModeBar': Constants.UI.PLOTLY_DISPLAY_MODE_BAR})

                    with goal_tab:
                        max_goals = monthly_player_status_summary[Constants.Status.GOAL].max()
                        min_goals = monthly_player_status_summary[Constants.Status.GOAL].min()
                        colors_goals = [Constants.UI.COLOR_GREEN if goals == max_goals else Constants.UI.COLOR_RED if goals == min_goals else Constants.UI.COLOR_LIGHTGRAY for goals in monthly_player_status_summary[Constants.Status.GOAL]]
                        fig_goals_monthly = px.bar(monthly_player_status_summary, x=Constants.Columns.SHOOTER_NAME, y=Constants.Status.GOAL,
                                                  title="Player Monthly Goals")
                        fig_goals_monthly.update_traces(marker_color=colors_goals)
                        fig_goals_monthly.update_layout(yaxis_title="Goals", xaxis_title="Player Name", xaxis=dict(fixedrange=Constants.UI.PLOTLY_FIXED_RANGE), yaxis=dict(fixedrange=Constants.UI.PLOTLY_FIXED_RANGE))
                        st.plotly_chart(fig_goals_monthly, use_container_width=True, config={'displayModeBar': Constants.UI.PLOTLY_DISPLAY_MODE_BAR})

                    with saved_tab:
                        max_saved = monthly_player_status_summary[Constants.Status.SAVED].max()
                        min_saved = monthly_player_status_summary[Constants.Status.SAVED].min()
                        colors_saved = [Constants.UI.COLOR_RED if saved == max_saved else Constants.UI.COLOR_GREEN if saved == min_saved else Constants.UI.COLOR_LIGHTGRAY for saved in monthly_player_status_summary[Constants.Status.SAVED]]
                        fig_saved_monthly = px.bar(monthly_player_status_summary, x=Constants.Columns.SHOOTER_NAME, y=Constants.Status.SAVED,
                                                  title="Player Monthly Saved Shots")
                        fig_saved_monthly.update_traces(marker_color=colors_saved)
                        fig_saved_monthly.update_layout(yaxis_title="Saved Shots", xaxis_title="Player Name", xaxis=dict(fixedrange=Constants.UI.PLOTLY_FIXED_RANGE), yaxis=dict(fixedrange=Constants.UI.PLOTLY_FIXED_RANGE))
                        st.plotly_chart(fig_saved_monthly, use_container_width=True, config={'displayModeBar': Constants.UI.PLOTLY_DISPLAY_MODE_BAR})

                with out_tab:
                    max_out = monthly_player_status_summary[Constants.Status.OUT].max()
                    min_out = monthly_player_status_summary[Constants.Status.OUT].min()
                    colors_out = [Constants.UI.COLOR_RED if out_val == max_out else Constants.UI.COLOR_GREEN if out_val == min_out else Constants.UI.COLOR_LIGHTGRAY for out_val in monthly_player_status_summary[Constants.Status.OUT]]
                    fig_out_monthly = px.bar(monthly_player_status_summary, x=Constants.Columns.SHOOTER_NAME, y=Constants.Status.OUT,
                                            title="Player Monthly Out Shots")
                    fig_out_monthly.update_traces(marker_color=colors_out)
                    fig_out_monthly.update_layout(yaxis_title="Out Shots", xaxis_title="Player Name", xaxis=dict(fixedrange=Constants.UI.PLOTLY_FIXED_RANGE), yaxis=dict(fixedrange=Constants.UI.PLOTLY_FIXED_RANGE))
                    st.plotly_chart(fig_out_monthly, use_container_width=True, config={'displayModeBar': Constants.UI.PLOTLY_DISPLAY_MODE_BAR})


            else:
                st.info(Constants.UI.INFO_NO_PLAYER_DATA.format(selected_month_display=selected_month_display))