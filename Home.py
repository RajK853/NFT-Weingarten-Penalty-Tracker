import streamlit as st
import plotly.express as px
from utils import load_data, calculate_goal_percentage, get_overall_statistics, calculate_save_percentage, get_overall_shoot_position_success, get_overall_trend_data, get_monthly_outcome_distribution, Constants

st.set_page_config(
    page_title="NFT Weingarten - Penalty Tracker",
)

col1, col2 = st.columns([1, 4])
with col1:
    st.image(Constants.LOGO_PATH, width=100)
with col2:
    st.title("Penalty Shootout Dashboard")

st.markdown(
        """
        This interactive dashboard visualizes penalty shootout data, offering insights into player performance and shot outcomes.
        Explore key statistics and trends from various penalty shootouts.
        """
    )

data = load_data()
total_penalties, overall_goal_percentage, outcome_distribution = get_overall_statistics(data)

st.subheader("Overall Shootout Statistics")
st.markdown("*(Showing statistics from the recent 30 days)*")

total_penalties, overall_goal_percentage, outcome_distribution = get_overall_statistics(data, num_periods=30, period_type="Days")

col_stats1, col_stats2 = st.columns(2)
with col_stats1:
    st.metric("Total Penalties", total_penalties)
with col_stats2:
    st.metric("Overall Goal Success", f"{overall_goal_percentage:.2f}%")

fig_outcome = px.pie(outcome_distribution, values=Constants.GOAL_PERCENTAGE_COL, names=Constants.STATUS_COL,
                     title="Outcome Distribution", hole=0.4)
fig_outcome.update_traces(textinfo='percent+label', pull=[0.05 if s == Constants.GOAL_STATUS else 0 for s in outcome_distribution[Constants.STATUS_COL]])
st.plotly_chart(fig_outcome, use_container_width=True)

st.subheader("Goal Percentage Leaderboard")
num_players = st.slider("Select number of top players to display", 5, 20, 10)
data = load_data()
top_players = calculate_goal_percentage(data).head(num_players)
fig_top_players = px.bar(top_players, x=top_players.index, y=Constants.GOAL_PERCENTAGE_COL,
                         title=f"Top {num_players} Players by Goal Percentage",
                         hover_data=[Constants.GOALS_COL, Constants.MISSES_COL, Constants.TOTAL_SHOTS_COL])
fig_top_players.update_layout(yaxis_title="Goal Percentage (%)", yaxis_range=[0, 100])
fig_top_players.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
st.plotly_chart(fig_top_players)

st.subheader("Goalkeeper Save Percentage Leaderboard")
num_keepers = st.slider("Select number of top goalkeepers to display", 5, 20, 10)
keeper_performance = calculate_save_percentage(data).head(num_keepers)
fig_top_keepers = px.bar(keeper_performance, x=keeper_performance.index, y=Constants.SAVE_PERCENTAGE_COL,
                         title=f"Top {num_keepers} Goalkeepers by Save Percentage",
                         hover_data=[Constants.TOTAL_SAVES_COL, Constants.TOTAL_FACED_COL])
fig_top_keepers.update_layout(yaxis_title="Save Percentage (%)", yaxis_range=[0, 100])
fig_top_keepers.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
st.plotly_chart(fig_top_keepers)

st.subheader("Overall Shoot Position Effectiveness")
shoot_position_success = get_overall_shoot_position_success(data)
fig_position_success = px.bar(shoot_position_success, x=shoot_position_success.index, y=Constants.GOAL_PERCENTAGE_COL,
                                title="Overall Goal Percentage by Shoot Position",
                                hover_data=[Constants.GOALS_COL, Constants.TOTAL_SHOTS_COL])
fig_position_success.update_layout(yaxis_title="Goal Percentage (%)", yaxis_range=[0, 100])
fig_position_success.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
st.plotly_chart(fig_position_success)

st.subheader("Monthly Goal Percentage Trend")
monthly_trend = get_overall_trend_data(data)
fig_monthly_trend = px.line(monthly_trend, x="Month", y=Constants.GOAL_PERCENTAGE_COL,
                              title="Overall Monthly Goal Percentage Trend")
fig_monthly_trend.update_layout(yaxis_title="Goal Percentage (%)", yaxis_range=[0, 100])
st.plotly_chart(fig_monthly_trend)

st.subheader("Monthly Outcome Distribution")
monthly_outcome_dist = get_monthly_outcome_distribution(data)
fig_monthly_outcome = px.bar(monthly_outcome_dist, x="Month", y=Constants.GOAL_PERCENTAGE_COL, color=Constants.STATUS_COL,
                               title="Monthly Distribution of Penalty Outcomes",
                               labels={Constants.GOAL_PERCENTAGE_COL: "Percentage", "Month": "Month"},
                               category_orders={Constants.STATUS_COL: [Constants.GOAL_STATUS, Constants.SAVED_STATUS, Constants.OUT_STATUS]})
fig_monthly_outcome.update_layout(yaxis_title="Percentage (%)", yaxis_range=[0, 100])
st.plotly_chart(fig_monthly_outcome)
