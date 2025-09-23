import pandas as pd
import streamlit as st
import plotly.express as px
from utils import load_data, get_overall_statistics, get_overall_trend_data, get_monthly_outcome_distribution, calculate_player_scores, calculate_save_percentage, Constants

st.set_page_config(
    page_title="NFT Weingarten - Penalty Tracker",
    page_icon="🏠",
)

col1, col2 = st.columns([1, 4])
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

st.subheader("Overall Penalty Statistics")
st.markdown(f"*(Showing statistics from the recent {Constants.RECENT_DAYS_FILTER} days)*")

total_penalties, overall_goal_percentage, outcome_distribution = get_overall_statistics(data, num_periods=Constants.RECENT_DAYS_FILTER, period_type=Constants.PERIOD_TYPE_DAYS)

col_stats1, col_stats2 = st.columns(2)
with col_stats1:
    st.metric("Total Penalties", total_penalties)
with col_stats2:
    st.metric("Overall Goal Success", f"{overall_goal_percentage:.2f}%")

# Homepage Insights
st.subheader("Top Performers (All Time)")

top_player_df = calculate_player_scores(data).head(1)
top_player_name = top_player_df.index[0]
top_player_score = top_player_df[Constants.SCORE_COL].iloc[0]

top_keeper_df = calculate_save_percentage(data).head(1)
top_keeper_name = top_keeper_df.index[0]
top_keeper_save_percentage = top_keeper_df[Constants.SAVE_PERCENTAGE_COL].iloc[0]

col_insight1, col_insight2 = st.columns(2)
with col_insight1:
    st.metric("Top Player", f"{top_player_name} ({top_player_score} points)")
with col_insight2:
    st.metric("Top Goalkeeper", f"{top_keeper_name} ({top_keeper_save_percentage:.2f}% saves)")

fig_outcome = px.pie(outcome_distribution, values=Constants.GOAL_PERCENTAGE_COL, names=Constants.STATUS_COL,
                     title="Outcome Distribution", hole=0.4)
fig_outcome.update_traces(textinfo='percent+label', pull=[Constants.PIE_CHART_PULL_EFFECT if s == Constants.GOAL_STATUS else 0 for s in outcome_distribution[Constants.STATUS_COL]])
st.plotly_chart(fig_outcome, use_container_width=True, config={'displayModeBar': False})



st.subheader("Monthly Outcome Trend")

col_date1, col_date2 = st.columns(2)
with col_date1:
    min_date = data[Constants.DATE_COL].min()
    max_date = data[Constants.DATE_COL].max()
    start_date_filter = st.date_input("Start date", value=min_date, min_value=min_date, max_value=max_date)
with col_date2:
    end_date_filter = st.date_input("End date", value=max_date, min_value=min_date, max_value=max_date)

monthly_trend_data = get_overall_trend_data(data, start_date=start_date_filter, end_date=end_date_filter)

fig_monthly_trend = px.line(monthly_trend_data, x=Constants.MONTH_COL, y=Constants.PERCENTAGE_COL, color=Constants.OUTCOME_TYPE_COL,
                            title="Monthly Outcome Trend", markers=True,
                            labels={Constants.PERCENTAGE_COL: "Percentage", Constants.MONTH_COL: "Month"},
                            animation_frame=Constants.MONTH_COL, animation_group=Constants.OUTCOME_TYPE_COL)
fig_monthly_trend.update_layout(yaxis_title="Percentage (%)", yaxis_range=[Constants.Y_AXIS_RANGE_MIN, Constants.Y_AXIS_RANGE_MAX], xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True))
st.plotly_chart(fig_monthly_trend, config={'displayModeBar': False})

monthly_outcome_dist = get_monthly_outcome_distribution(data, start_date=start_date_filter, end_date=end_date_filter)
fig_monthly_outcome = px.bar(monthly_outcome_dist, x=Constants.MONTH_COL, y=Constants.GOAL_PERCENTAGE_COL, color=Constants.STATUS_COL,
                               title="Monthly Outcome Distribution",
                               labels={Constants.GOAL_PERCENTAGE_COL: "Percentage", Constants.MONTH_COL: "Month"},
                               category_orders={Constants.STATUS_COL: [Constants.GOAL_STATUS, Constants.SAVED_STATUS, Constants.OUT_STATUS]},
                               animation_frame=Constants.MONTH_COL, animation_group=Constants.STATUS_COL)
fig_monthly_outcome.update_layout(yaxis_title="Percentage (%)", yaxis_range=[Constants.Y_AXIS_RANGE_MIN, Constants.Y_AXIS_RANGE_MAX], xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True))
st.plotly_chart(fig_monthly_outcome, config={'displayModeBar': False})