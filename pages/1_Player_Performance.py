"""
Streamlit page for analyzing player performance in penalties.
"""

from datetime import date
from typing import List

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from src import analysis
from src import ui
from src.constants import Columns, Data, Scoring, Status, UI

ui.setup_page(
    page_title="NFT Weingarten - Player Performance",
    page_icon=UI.EMOJI_PLAYER_PAGE,
    page_description="""
    Here you can analyze how well individual players are doing. 
    Use the tools below to compare players and see who is performing best over time.
    """,
)

data: pd.DataFrame = ui.load_and_process_data()

with st.container(border=True):
    st.subheader("Player Score Leaderboard")
    st.markdown(
        "This leaderboard ranks players by score. A higher score means better performance."
    )
    st.info(
        f"Scores are weighted by how recent they are. The current half-life is {Scoring.PERFORMANCE_HALF_LIFE_DAYS} days. This means recent scores are more important."
    )

    st.markdown(
        "For a detailed explanation of the scoring system, please visit the [Scoring Method](/Scoring_Method) page."
    )

    st.markdown(
        "Use the date range selector to analyze performance during specific periods."
    )

    min_date_leaderboard = data[Columns.DATE].min()
    max_date_leaderboard = data[Columns.DATE].max()

    selected_date_range = st.date_input(
        "Select date range for Leaderboard",
        value=[min_date_leaderboard, max_date_leaderboard],
        min_value=min_date_leaderboard,
        max_value=max_date_leaderboard,
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
        score_format_specifier = f".{Data.SCORE_DECIMAL_PLACES}f"
        top_players: pd.DataFrame = analysis.calculate_player_scores(
            data, start_date=leaderboard_start_date, end_date=leaderboard_end_date
        ).head(UI.TOP_N_PLAYERS_LEADERBOARD)
        fig_top_players = px.bar(
            top_players,
            x=top_players.index,
            y=Columns.SCORE,
            title=f"Top {UI.TOP_N_PLAYERS_LEADERBOARD} Players by Score",
            hover_data=[Status.GOAL, Status.SAVED, Status.OUT],
        )
        ui.configure_plotly_layout(fig_top_players, top_players[Columns.SCORE], yaxis_title="Score")  # fixedrange will be applied by render_plotly_chart
        fig_top_players.update_traces(
            texttemplate=f"%{{y:{score_format_specifier}}}",
            textposition=UI.PLOTLY_TEXT_POSITION_OUTSIDE,
        )
        ui.render_plotly_chart(fig_top_players, fixed_range=True)
        st.dataframe(
            top_players,
            column_config={
                Columns.SCORE: st.column_config.NumberColumn(
                    format=f"%.{Data.SCORE_DECIMAL_PLACES}f"
                )
            },
        )

    else:
        st.info(UI.INFO_SELECT_DATE_RANGE)

    st.subheader("Compare Player Performance Over Time")
    st.markdown(
        "Choose players and a month to see how they performed. You can see their score, goals, saved shots, and missed shots."
    )
    player_names: List[str] = list(sorted(data[Columns.SHOOTER_NAME].unique()))
    selected_players: List[str] = st.multiselect(
        f"Select up to {UI.MAX_PLAYER_SELECTIONS} Players to Compare",
        player_names,
        default=player_names[: UI.DEFAULT_NUM_PLAYERS_MULTISELECT],
        max_selections=UI.MAX_PLAYER_SELECTIONS,
    )

    # Generate unique months for the dropdown
    data[Columns.MONTH] = pd.to_datetime(data[Columns.DATE]).dt.to_period("M")
    unique_months_period: List[pd.Period] = sorted(
        data[Columns.MONTH].unique(), reverse=True
    )
    unique_months_display: List[str] = [
        month.strftime("%B %Y") for month in unique_months_period
    ]

    selected_month_display: str = st.selectbox("Select a Month", unique_months_display)

    # Determine start and end dates for the selected month
    if selected_month_display:
        start_date_filter, end_date_filter = analysis._get_date_range_from_month_display(
            selected_month_display
        )

        if selected_players:
            st.subheader("Performance Over Time")

            player_status_data: pd.DataFrame = analysis.get_player_status_counts_over_time(
                data,
                selected_players,
                start_date=start_date_filter,
                end_date=end_date_filter,
            )
            player_status_data[Columns.MONTH] = (
                pd.to_datetime(player_status_data[Columns.DATE])
                .dt.to_period("M")
                .astype(str)
            )

            if not player_status_data.empty:
                # Aggregate data by player and status for the entire month
                monthly_player_status_summary: pd.DataFrame = (
                    player_status_data.groupby(
                        [Columns.MONTH, Columns.SHOOTER_NAME, Columns.STATUS]
                    )[Columns.COUNT]
                    .sum()
                    .unstack(fill_value=Data.DEFAULT_FILL_VALUE)
                    .reset_index()
                )

                # Calculate total shots for each player in the month
                monthly_player_status_summary[Columns.TOTAL_SHOTS] = (
                    monthly_player_status_summary[Status.GOAL]
                    + monthly_player_status_summary[Status.SAVED]
                    + monthly_player_status_summary[Status.OUT]
                )

                # Calculate score for each player
                monthly_player_status_summary[Columns.SCORE] = (
                    (monthly_player_status_summary[Status.GOAL] * Scoring.GOAL)
                    + (monthly_player_status_summary[Status.SAVED] * Scoring.SAVED)
                    + (monthly_player_status_summary[Status.OUT] * Scoring.OUT)
                )

                if not monthly_player_status_summary.empty:
                    score_tab, goal_tab, saved_tab, out_tab = st.tabs(
                        [UI.TAB_SCORE, UI.TAB_GOALS, UI.TAB_SAVED, UI.TAB_OUT]
                    )
                    with score_tab:
                        max_score = monthly_player_status_summary[Columns.SCORE].max()
                        min_score = monthly_player_status_summary[Columns.SCORE].min()
                        colors_score = [
                            (
                                UI.COLOR_GREEN
                                if score == max_score
                                else (
                                    UI.COLOR_RED
                                    if score == min_score
                                    else UI.COLOR_LIGHTGRAY
                                )
                            )
                            for score in monthly_player_status_summary[Columns.SCORE]
                        ]
                        fig_score_monthly = px.bar(
                            monthly_player_status_summary,
                            x=Columns.SHOOTER_NAME,
                            y=Columns.SCORE,
                            title="Player Monthly Score",
                        )
                        fig_score_monthly.update_traces(
                            texttemplate=f"%{{y:{score_format_specifier}}}"
                        )
                        ui.configure_plotly_layout(fig_score_monthly, monthly_player_status_summary[Columns.SCORE], yaxis_title="Score", xaxis_title="Player Name")  # fixedrange will be applied by render_plotly_chart
                        ui.render_plotly_chart(fig_score_monthly, fixed_range=True)

                    with goal_tab:
                        max_goals = monthly_player_status_summary[Status.GOAL].max()
                        min_goals = monthly_player_status_summary[Status.GOAL].min()
                        colors_goals = [
                            (
                                UI.COLOR_GREEN
                                if goals == max_goals
                                else (
                                    UI.COLOR_RED
                                    if goals == min_goals
                                    else UI.COLOR_LIGHTGRAY
                                )
                            )
                            for goals in monthly_player_status_summary[Status.GOAL]
                        ]
                        fig_goals_monthly = px.bar(
                            monthly_player_status_summary,
                            x=Columns.SHOOTER_NAME,
                            y=Status.GOAL,
                            title="Player Monthly Goals",
                        )
                        fig_goals_monthly.update_traces(marker_color=colors_goals)
                        ui.configure_plotly_layout(fig_goals_monthly, monthly_player_status_summary[Status.GOAL], yaxis_title="Goals", xaxis_title="Player Name")  # fixedrange will be applied by render_plotly_chart
                        ui.render_plotly_chart(fig_goals_monthly, fixed_range=True)

                    with saved_tab:
                        max_saved = monthly_player_status_summary[Status.SAVED].max()
                        min_saved = monthly_player_status_summary[Status.SAVED].min()
                        colors_saved = [
                            (
                                UI.COLOR_RED
                                if saved == max_saved
                                else (
                                    UI.COLOR_GREEN
                                    if saved == min_saved
                                    else UI.COLOR_LIGHTGRAY
                                )
                            )
                            for saved in monthly_player_status_summary[Status.SAVED]
                        ]
                        fig_saved_monthly = px.bar(
                            monthly_player_status_summary,
                            x=Columns.SHOOTER_NAME,
                            y=Status.SAVED,
                            title="Player Monthly Saved Shots",
                        )
                        fig_saved_monthly.update_traces(marker_color=colors_saved)
                        ui.configure_plotly_layout(fig_saved_monthly, monthly_player_status_summary[Status.SAVED], yaxis_title="Saved Shots", xaxis_title="Player Name")  # fixedrange will be applied by render_plotly_chart
                        ui.render_plotly_chart(fig_saved_monthly, fixed_range=True)

                with out_tab:
                    max_out = monthly_player_status_summary[Status.OUT].max()
                    min_out = monthly_player_status_summary[Status.OUT].min()
                    colors_out = [
                        (
                            UI.COLOR_RED
                            if out_val == max_out
                            else (
                                UI.COLOR_GREEN
                                if out_val == min_out
                                else UI.COLOR_LIGHTGRAY
                            )
                        )
                        for out_val in monthly_player_status_summary[Status.OUT]
                    ]
                    fig_out_monthly = px.bar(
                        monthly_player_status_summary,
                        x=Columns.SHOOTER_NAME,
                        y=Status.OUT,
                        title="Player Monthly Out Shots",
                    )
                    fig_out_monthly.update_traces(marker_color=colors_out)
                    ui.configure_plotly_layout(fig_out_monthly, monthly_player_status_summary[Status.OUT], yaxis_title="Out Shots", xaxis_title="Player Name")  # fixedrange will be applied by render_plotly_chart
                    ui.render_plotly_chart(fig_out_monthly, fixed_range=True)

            else:
                st.info(
                    UI.INFO_NO_PLAYER_DATA.format(
                        selected_month_display=selected_month_display
                    )
                )
