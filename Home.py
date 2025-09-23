import pandas as pd
import streamlit as st
import plotly.express as px
from utils import load_data, get_overall_statistics, get_monthly_outcome_distribution, calculate_player_scores, calculate_save_percentage, Constants

st.set_page_config(
    page_title="NFT Weingarten - Penalty Tracker",
    page_icon=Constants.EMOJI_HOME_PAGE,
)

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

data = load_data()

# Convert 'Date' column to datetime objects and extract only the date part
data[Constants.DATE_COL] = pd.to_datetime(data[Constants.DATE_COL]).dt.date

# Homepage Insights
st.subheader("Top Performers")
st.markdown(f"*(Showing statistics from the recent {Constants.RECENT_DAYS_FILTER} days)*")
st.markdown("Discover the top-performing player and goalkeeper based on recent penalty shootout data. This section highlights individuals who have demonstrated exceptional skill in scoring or saving penalties over the last month, providing a quick snapshot of current form.")

current_date = pd.to_datetime(data[Constants.DATE_COL]).max()
start_date_top_performers = (current_date - pd.DateOffset(days=Constants.RECENT_DAYS_FILTER)).date()
end_date_top_performers = current_date.date()

top_player_df = calculate_player_scores(data, start_date=start_date_top_performers, end_date=end_date_top_performers).head(1)
top_player_name = top_player_df.index[0]
top_player_score = top_player_df[Constants.SCORE_COL].iloc[0]

top_keeper_df = calculate_save_percentage(data, start_date=start_date_top_performers, end_date=end_date_top_performers).head(1)
top_keeper_name = top_keeper_df.index[0]
top_keeper_save_percentage = top_keeper_df[Constants.SAVE_PERCENTAGE_COL].iloc[0]

col_insight1, col_insight2 = st.columns(2)
with col_insight1:
    st.text("Top Player")
    st.markdown(f"<h1 style='{Constants.GOLD_TEXT_STYLE}'>{top_player_name}</h1>", unsafe_allow_html=True)
    st.text(f"{top_player_score} points")
with col_insight2:
    st.text("Top Goalkeeper")
    st.markdown(f"<h1 style='{Constants.GOLD_TEXT_STYLE}'>{top_keeper_name}</h1>", unsafe_allow_html=True)
    st.text(f"{top_keeper_save_percentage:.1f}% saves")

st.subheader("Overall Penalty Statistics")
st.markdown(f"*(Showing statistics from the recent {Constants.RECENT_DAYS_FILTER} days)*")
st.markdown("This section provides an overview of penalty outcomes, showing the distribution of goals, saves, and shots out, along with their absolute counts. Gain insights into the overall success rate and how different outcomes contribute to the total penalty events.")

total_penalties, overall_goal_percentage, outcome_distribution = get_overall_statistics(data, num_periods=Constants.RECENT_DAYS_FILTER, period_type=Constants.PERIOD_TYPE_DAYS)

col_stats1, col_stats2 = st.columns(2)
with col_stats1:
    st.metric("Total Penalties", total_penalties, help="The total number of penalties recorded within the selected period.")
with col_stats2:
    st.metric("Overall Goal Success", f"{overall_goal_percentage:.2f}%", help="The percentage of penalties that resulted in a goal.")

fig_outcome = px.pie(outcome_distribution, values=Constants.GOAL_PERCENTAGE_COL, names=Constants.STATUS_COL,
                        title="Outcome Distribution", hole=Constants.PIE_CHART_HOLE_SIZE)
fig_outcome.update_traces(textinfo='percent+label', pull=[Constants.PIE_CHART_PULL_EFFECT if s == Constants.GOAL_STATUS else 0 for s in outcome_distribution[Constants.STATUS_COL]])
st.plotly_chart(fig_outcome, use_container_width=True, config={'displayModeBar': Constants.PLOTLY_DISPLAY_MODE_BAR})

