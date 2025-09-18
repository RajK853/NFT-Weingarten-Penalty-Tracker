import pandas as pd
import streamlit as st
import plotly.express as px
from utils import load_data, calculate_goal_percentage, get_overall_statistics, calculate_save_percentage, get_overall_shoot_position_success, get_overall_trend_data, get_monthly_outcome_distribution, get_keeper_outcome_distribution, Constants

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

# Convert 'Date' column to datetime objects and extract only the date part
data[Constants.DATE_COL] = pd.to_datetime(data[Constants.DATE_COL]).dt.date

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
num_players = 10

num_months_filter = st.slider("Filter for recent N months", 1, 12, 12)
top_players = calculate_goal_percentage(data, num_months=num_months_filter).head(num_players)
fig_top_players = px.bar(top_players, x=top_players.index, y=Constants.GOAL_PERCENTAGE_COL,
                         title=f"Top {num_players} Players by Goal Percentage (Recent {num_months_filter} Months)",
                         hover_data=[Constants.GOALS_COL, Constants.MISSES_COL, Constants.TOTAL_SHOTS_COL])
fig_top_players.update_layout(yaxis_title="Goal Percentage (%)", yaxis_range=[0, 100])
fig_top_players.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
st.plotly_chart(fig_top_players)

st.subheader("Goalkeeper Performance Analysis")

keeper_performance_all = calculate_save_percentage(data)
top_5_keepers = keeper_performance_all.head(5).index.tolist()

# Create columns dynamically based on the number of top 5 goalkeepers
cols = st.columns(len(top_5_keepers))

for i, keeper in enumerate(top_5_keepers):
    with cols[i]:
        keeper_outcome_dist = get_keeper_outcome_distribution(data, keeper)
        if not keeper_outcome_dist.empty:
            fig_keeper_outcome = px.pie(keeper_outcome_dist, values=Constants.COUNT_COL, names=Constants.STATUS_COL,
                                        title=f"{keeper}'s Outcome Distribution", hole=0.4)
            fig_keeper_outcome.update_traces(textinfo='percent+label', pull=[0.05 if s == Constants.GOAL_STATUS else 0 for s in keeper_outcome_dist[Constants.STATUS_COL]])
            st.plotly_chart(fig_keeper_outcome, use_container_width=True)
        else:
            st.info(f"No data available for {keeper}.")

st.subheader("Overall Shoot Position Effectiveness")
shoot_position_success = get_overall_shoot_position_success(data)
fig_position_success = px.bar(shoot_position_success, x=shoot_position_success.index, y=Constants.GOAL_PERCENTAGE_COL,
                                title="Overall Goal Percentage by Shoot Position",
                                hover_data=[Constants.GOALS_COL, Constants.TOTAL_SHOTS_COL])
fig_position_success.update_layout(yaxis_title="Goal Percentage (%)", yaxis_range=[0, 100])
fig_position_success.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
st.plotly_chart(fig_position_success)

st.subheader("Monthly Outcome Trend")

col_date1, col_date2 = st.columns(2)
with col_date1:
    min_date = data[Constants.DATE_COL].min()
    max_date = data[Constants.DATE_COL].max()
    start_date_filter = st.date_input("Start date", value=min_date, min_value=min_date, max_value=max_date)
with col_date2:
    end_date_filter = st.date_input("End date", value=max_date, min_value=min_date, max_value=max_date)

monthly_trend_data = get_overall_trend_data(data, start_date=start_date_filter, end_date=end_date_filter)

if not monthly_trend_data.empty:
    fig_monthly_trend = px.line(monthly_trend_data, x="Month", y="Percentage", color="Outcome Type",
                                  title="Monthly Trend of Penalty Outcomes",
                                  category_orders={"Outcome Type": ["Goal Percentage", "Saved Percentage", "Out Percentage"]})
    fig_monthly_trend.update_layout(yaxis_title="Percentage (%)", yaxis_range=[0, 100])
    fig_monthly_trend.update_traces(line=dict(width=3)) # Make lines bold
    st.plotly_chart(fig_monthly_trend)
else:
    st.info("No data available for the selected date range.")

st.subheader("Monthly Outcome Distribution")
monthly_outcome_dist = get_monthly_outcome_distribution(data)
fig_monthly_outcome = px.bar(monthly_outcome_dist, x="Month", y=Constants.GOAL_PERCENTAGE_COL, color=Constants.STATUS_COL,
                               title="Monthly Distribution of Penalty Outcomes",
                               labels={Constants.GOAL_PERCENTAGE_COL: "Percentage", "Month": "Month"},
                               category_orders={Constants.STATUS_COL: [Constants.GOAL_STATUS, Constants.SAVED_STATUS, Constants.OUT_STATUS]})
fig_monthly_outcome.update_layout(yaxis_title="Percentage (%)", yaxis_range=[0, 100])
st.plotly_chart(fig_monthly_outcome)
