import pandas as pd
import streamlit as st
import plotly.express as px
from utils import load_data, get_overall_statistics, calculate_player_scores, calculate_save_percentage, Constants

st.set_page_config(
    page_title="NFT Weingarten - Penalty Tracker",
    page_icon=Constants.EMOJI_HOME_PAGE,
    initial_sidebar_state="expanded",
    layout="wide"
)

# --- Header ---
col1, col2 = st.columns(Constants.HOME_PAGE_COLUMN_RATIO)
with col1:
    st.image(Constants.LOGO_PATH, width=Constants.LOGO_WIDTH)
with col2:
    st.title("Penalty Dashboard")

st.markdown(
    """
    This interactive dashboard visualizes penalty data, offering insights into player performance and shot outcomes.
    Explore key statistics and trends from various penalties.
    """
)

st.markdown("---")

# --- Load Data ---
data = load_data()
data[Constants.DATE_COL] = pd.to_datetime(data[Constants.DATE_COL]).dt.date

# --- Main Content ---
col_main1, col_main2 = st.columns(2, gap="large")

with col_main1:
    with st.container(border=True):
        st.subheader("Overall Penalty Statistics")
        st.markdown(f"*(Showing statistics from the recent {Constants.RECENT_DAYS_FILTER} days)*")

        _, _, outcome_distribution = get_overall_statistics(data, num_periods=Constants.RECENT_DAYS_FILTER, period_type=Constants.PERIOD_TYPE_DAYS)

        fig_outcome = px.pie(outcome_distribution, values=Constants.GOAL_PERCENTAGE_COL, names=Constants.STATUS_COL,
                               title="Outcome Distribution", hole=Constants.PIE_CHART_HOLE_SIZE)
        fig_outcome.update_traces(textinfo='percent+label', pull=[Constants.PIE_CHART_PULL_EFFECT if s == Constants.GOAL_STATUS else 0 for s in outcome_distribution[Constants.STATUS_COL]])
        st.plotly_chart(fig_outcome, use_container_width=True, config={'displayModeBar': Constants.PLOTLY_DISPLAY_MODE_BAR})

with col_main2:
    with st.container(border=True):
        st.subheader("Top Performers", help=f"Recent {Constants.RECENT_DAYS_FILTER} days)")
        
        current_date = pd.to_datetime(data[Constants.DATE_COL]).max()
        start_date_top_performers = (current_date - pd.DateOffset(days=Constants.RECENT_DAYS_FILTER)).date()
        end_date_top_performers = current_date.date()

        top_player_df = calculate_player_scores(data, start_date=start_date_top_performers, end_date=end_date_top_performers).head(1)
        top_player_name = top_player_df.index[0]
        top_player_score = top_player_df[Constants.SCORE_COL].iloc[0]

        top_keeper_df = calculate_save_percentage(data, start_date=start_date_top_performers, end_date=end_date_top_performers).head(1)
        top_keeper_name = top_keeper_df.index[0]
        top_keeper_save_percentage = top_keeper_df[Constants.SAVE_PERCENTAGE_COL].iloc[0]

        performer_col1, performer_col2 = st.columns(2)
        with performer_col1:
            with st.expander("🏆 Top Player", expanded=False):
                st.metric(
                    label="Score",
                    value=top_player_name,
                    delta=f"{top_player_score} points",
                    help=f"The player's score is calculated based on the outcome of their shots (goal: {Constants.GOAL_SCORE:.1f}, saved: {Constants.SAVED_SCORE:.1f}, out: {Constants.OUT_SCORE:.1f})."
                )
        with performer_col2:
            with st.expander("🧤 Top Goalkeeper", expanded=False):
                st.metric(
                    label="Save Percentage",
                    value=top_keeper_name,
                    delta=f"{top_keeper_save_percentage:.1f}% saves",
                    help="The percentage of penalties faced by the goalkeeper that were saved."
                )