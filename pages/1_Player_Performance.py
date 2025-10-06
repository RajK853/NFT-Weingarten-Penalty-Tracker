"""
Streamlit page for analyzing player performance in penalties.
"""
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from src.data_loader import load_data
from src.analysis import get_player_status_counts_over_time, calculate_player_scores, _get_date_range_from_month_display
from src.constants import Columns, Data, Paths, Scoring, Status, UI
from src.ui import gender_selection_ui, data_refresh_button_ui
from typing import List
from datetime import date

st.set_page_config(
    page_title="NFT Weingarten - Player Performance",
    page_icon=UI.EMOJI_PLAYER_PAGE,
    initial_sidebar_state="expanded",
    layout="wide"
)

# --- Header ---

col1, col2, col3 = st.columns([1,0.5,1])
with col2:
    st.image(Paths.LOGO, width='stretch')

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
last_refresh_time = data_refresh_button_ui()
data: pd.DataFrame = load_data(gender=gender_selection, last_refresh_time=last_refresh_time)
data[Columns.DATE] = pd.to_datetime(data[Columns.DATE]).dt.date

with st.container(border=True):
    st.subheader("Player Score Leaderboard")
    st.markdown("This leaderboard ranks players based on a comprehensive scoring system that assigns points for each shot outcome (Goal, Saved, Out). A higher score indicates superior overall performance in penalty shootouts.")
    st.info(f"Scores are weighted by recency. The current performance half-life is {Scoring.PERFORMANCE_HALF_LIFE_DAYS} days.")

    # Scoring system explanation
    scoring_data = {
        'Outcome': [UI.TAB_GOALS, UI.TAB_SAVED, UI.TAB_OUT],
        'Points': [Scoring.GOAL, Scoring.SAVED, Scoring.OUT]
    }
    scoring_df = pd.DataFrame(scoring_data)
    st.dataframe(scoring_df, hide_index=True)

    with st.expander("How is the Time-Weighted Score Calculated?"):
            st.markdown("""
            To better reflect a player's current form, scores are weighted based on how recently they occurred. This is done using an **exponential decay** model, where the weight of a score decreases as it gets older.

            The formula used is:
            ```
            Weighted Score = Original Score * e^(-decay_rate * days_ago)
            ```
            The `decay_rate` is what controls how quickly the score value decreases. For simplicity, we configure this using a "half-life" value (currently **{Scoring.PERFORMANCE_HALF_LIFE_DAYS} days**), which is then converted to a decay rate for the actual leaderboard calculations.
            """)
            st.markdown("--- ")
            st.subheader("Decay Curve Comparison")
            st.markdown("Adjust the parameters for the **Simulation** curve (solid line) and compare it to the application's **Current Setting** (dashed line).")

            # --- Interactive Inputs ---
            col1, col2 = st.columns(2)
            with col1:
                original_score_input = st.number_input("Original Score", value=1.5, step=0.5, key="sim_score")
            with col2:
                decay_rate_input = st.number_input("Simulation Decay Rate", value=0.020, min_value=0.0, step=0.005, format="%.3f", key="sim_decay")

            # --- Plot Generation ---
            days_range = np.arange(0, 366)

            # --- Current Setting Data ---
            setting_scores = original_score_input * np.exp(-Scoring.DECAY_RATE * days_range)
            setting_df = pd.DataFrame({
                'Days Ago': days_range,
                'Weighted Score': setting_scores,
                'Curve': "Current Setting"
            })

            # --- Simulation Data ---
            simulation_scores = original_score_input * np.exp(-decay_rate_input * days_range)
            simulation_df = pd.DataFrame({
                'Days Ago': days_range,
                'Weighted Score': simulation_scores,
                'Curve': 'Simulation'
            })

            # --- Combine and Plot ---
            combined_df = pd.concat([setting_df, simulation_df])
            fig = px.line(
                combined_df, 
                x='Days Ago', 
                y='Weighted Score', 
                color='Curve', 
                line_dash='Curve', 
                title='Decay Curve Comparison',
                line_dash_map={"Current Setting": "dash", "Simulation": "solid"}
            )

            # --- Add Half-Life Markers ---
            # Current Setting Half-Life
            if Scoring.DECAY_RATE > 0:
                setting_half_life = np.log(2) / Scoring.DECAY_RATE
                fig.add_scatter(x=[setting_half_life], y=[original_score_input/2], mode='markers', marker=dict(size=10, color='blue'), name=f"Current Setting Half-Life ({setting_half_life:.1f} days)")

            # Simulation Half-Life
            if decay_rate_input > 0:
                sim_half_life = np.log(2) / decay_rate_input
                fig.add_scatter(x=[sim_half_life], y=[original_score_input/2], mode='markers', marker=dict(size=10, color='red'), name=f"Simulation Half-Life ({sim_half_life:.1f} days)")

            st.plotly_chart(fig, use_container_width=True)


    st.markdown("Use the date range selector to analyze performance during specific periods.")
    
    min_date_leaderboard = data[Columns.DATE].min()
    max_date_leaderboard = data[Columns.DATE].max()

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
        score_format_specifier = f".{Data.SCORE_DECIMAL_PLACES}f"
        top_players: pd.DataFrame = calculate_player_scores(data, start_date=leaderboard_start_date, end_date=leaderboard_end_date).head(UI.TOP_N_PLAYERS_LEADERBOARD)
        fig_top_players = px.bar(top_players, x=top_players.index, y=Columns.SCORE,
                                 title=f"Top {UI.TOP_N_PLAYERS_LEADERBOARD} Players by Score",
                                 hover_data=[Status.GOAL, Status.SAVED, Status.OUT])
        min_score_val = top_players[Columns.SCORE].min()
        max_score_val = top_players[Columns.SCORE].max()
        buffer = (max_score_val - min_score_val) * UI.CHART_Y_AXIS_BUFFER # 10% buffer
        y_range_min = min_score_val - buffer
        y_range_max = max_score_val + buffer
        fig_top_players.update_layout(yaxis_title="Score", xaxis=dict(fixedrange=UI.PLOTLY_FIXED_RANGE), yaxis=dict(range=[y_range_min, y_range_max]))
        fig_top_players.update_traces(texttemplate=f'%{{y:{score_format_specifier}}}', textposition=UI.PLOTLY_TEXT_POSITION_OUTSIDE)
        st.plotly_chart(fig_top_players, config={'displayModeBar': UI.PLOTLY_DISPLAY_MODE_BAR})
        st.dataframe(top_players, column_config={Columns.SCORE: st.column_config.NumberColumn(format=f"%.{Data.SCORE_DECIMAL_PLACES}f")})
        
    else:
        st.info(UI.INFO_SELECT_DATE_RANGE)

    st.subheader("Compare Player Performance Over Time")
    st.markdown("Select multiple players and a specific month to analyze their aggregated performance across different outcome categories (Score, Goals, Saved, Out). This section provides a detailed breakdown of how selected players performed within the chosen timeframe.")
    player_names: List[str] = list(sorted(data[Columns.SHOOTER_NAME].unique()))
    selected_players: List[str] = st.multiselect(
        f"Select up to {UI.MAX_PLAYER_SELECTIONS} Players to Compare",
        player_names,
        default=player_names[:UI.DEFAULT_NUM_PLAYERS_MULTISELECT],
        max_selections=UI.MAX_PLAYER_SELECTIONS,
    )

    # Generate unique months for the dropdown
    data[Columns.MONTH] = pd.to_datetime(data[Columns.DATE]).dt.to_period('M')
    unique_months_period: List[pd.Period] = sorted(data[Columns.MONTH].unique(), reverse=True)
    unique_months_display: List[str] = [month.strftime("%B %Y") for month in unique_months_period]

    selected_month_display: str = st.selectbox("Select a Month", unique_months_display)

    # Determine start and end dates for the selected month
    if selected_month_display:
        start_date_filter, end_date_filter = _get_date_range_from_month_display(selected_month_display)

        if selected_players:
            st.subheader("Performance Over Time")

            player_status_data: pd.DataFrame = get_player_status_counts_over_time(data, selected_players, start_date=start_date_filter, end_date=end_date_filter)
            player_status_data[Columns.MONTH] = pd.to_datetime(player_status_data[Columns.DATE]).dt.to_period('M').astype(str)

            if not player_status_data.empty:
                # Aggregate data by player and status for the entire month
                monthly_player_status_summary: pd.DataFrame = player_status_data.groupby([Columns.MONTH, Columns.SHOOTER_NAME, Columns.STATUS])[Columns.COUNT].sum().unstack(fill_value=Data.DEFAULT_FILL_VALUE).reset_index()

                # Calculate total shots for each player in the month
                monthly_player_status_summary[Columns.TOTAL_SHOTS] = monthly_player_status_summary[Status.GOAL] + monthly_player_status_summary[Status.SAVED] + monthly_player_status_summary[Status.OUT]

                # Calculate score for each player
                monthly_player_status_summary[Columns.SCORE] = (monthly_player_status_summary[Status.GOAL] * Scoring.GOAL) + (monthly_player_status_summary[Status.SAVED] * Scoring.SAVED) + (monthly_player_status_summary[Status.OUT] * Scoring.OUT)

                if not monthly_player_status_summary.empty:
                    score_tab, goal_tab, saved_tab, out_tab = st.tabs([UI.TAB_SCORE, UI.TAB_GOALS, UI.TAB_SAVED, UI.TAB_OUT])
                    with score_tab:
                        max_score = monthly_player_status_summary[Columns.SCORE].max()
                        min_score = monthly_player_status_summary[Columns.SCORE].min()
                        colors_score = [UI.COLOR_GREEN if score == max_score else UI.COLOR_RED if score == min_score else UI.COLOR_LIGHTGRAY for score in monthly_player_status_summary[Columns.SCORE]]
                        fig_score_monthly = px.bar(monthly_player_status_summary, x=Columns.SHOOTER_NAME, y=Columns.SCORE,
                                                  title="Player Monthly Score")
                        fig_score_monthly.update_traces(texttemplate=f'%{{y:{score_format_specifier}}}')
                        fig_score_monthly.update_layout(yaxis_title="Score", xaxis_title="Player Name", xaxis=dict(fixedrange=UI.PLOTLY_FIXED_RANGE), yaxis=dict(fixedrange=UI.PLOTLY_FIXED_RANGE))
                        st.plotly_chart(fig_score_monthly, use_container_width=True, config={'displayModeBar': UI.PLOTLY_DISPLAY_MODE_BAR})

                    with goal_tab:
                        max_goals = monthly_player_status_summary[Status.GOAL].max()
                        min_goals = monthly_player_status_summary[Status.GOAL].min()
                        colors_goals = [UI.COLOR_GREEN if goals == max_goals else UI.COLOR_RED if goals == min_goals else UI.COLOR_LIGHTGRAY for goals in monthly_player_status_summary[Status.GOAL]]
                        fig_goals_monthly = px.bar(monthly_player_status_summary, x=Columns.SHOOTER_NAME, y=Status.GOAL,
                                                  title="Player Monthly Goals")
                        fig_goals_monthly.update_traces(marker_color=colors_goals)
                        fig_goals_monthly.update_layout(yaxis_title="Goals", xaxis_title="Player Name", xaxis=dict(fixedrange=UI.PLOTLY_FIXED_RANGE), yaxis=dict(fixedrange=UI.PLOTLY_FIXED_RANGE))
                        st.plotly_chart(fig_goals_monthly, use_container_width=True, config={'displayModeBar': UI.PLOTLY_DISPLAY_MODE_BAR})

                    with saved_tab:
                        max_saved = monthly_player_status_summary[Status.SAVED].max()
                        min_saved = monthly_player_status_summary[Status.SAVED].min()
                        colors_saved = [UI.COLOR_RED if saved == max_saved else UI.COLOR_GREEN if saved == min_saved else UI.COLOR_LIGHTGRAY for saved in monthly_player_status_summary[Status.SAVED]]
                        fig_saved_monthly = px.bar(monthly_player_status_summary, x=Columns.SHOOTER_NAME, y=Status.SAVED,
                                                  title="Player Monthly Saved Shots")
                        fig_saved_monthly.update_traces(marker_color=colors_saved)
                        fig_saved_monthly.update_layout(yaxis_title="Saved Shots", xaxis_title="Player Name", xaxis=dict(fixedrange=UI.PLOTLY_FIXED_RANGE), yaxis=dict(fixedrange=UI.PLOTLY_FIXED_RANGE))
                        st.plotly_chart(fig_saved_monthly, use_container_width=True, config={'displayModeBar': UI.PLOTLY_DISPLAY_MODE_BAR})

                with out_tab:
                    max_out = monthly_player_status_summary[Status.OUT].max()
                    min_out = monthly_player_status_summary[Status.OUT].min()
                    colors_out = [UI.COLOR_RED if out_val == max_out else UI.COLOR_GREEN if out_val == min_out else UI.COLOR_LIGHTGRAY for out_val in monthly_player_status_summary[Status.OUT]]
                    fig_out_monthly = px.bar(monthly_player_status_summary, x=Columns.SHOOTER_NAME, y=Status.OUT,
                                            title="Player Monthly Out Shots")
                    fig_out_monthly.update_traces(marker_color=colors_out)
                    fig_out_monthly.update_layout(yaxis_title="Out Shots", xaxis_title="Player Name", xaxis=dict(fixedrange=UI.PLOTLY_FIXED_RANGE), yaxis=dict(fixedrange=UI.PLOTLY_FIXED_RANGE))
                    st.plotly_chart(fig_out_monthly, use_container_width=True, config={'displayModeBar': UI.PLOTLY_DISPLAY_MODE_BAR})


            else:
                st.info(UI.INFO_NO_PLAYER_DATA.format(selected_month_display=selected_month_display))