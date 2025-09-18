import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data, get_player_status_counts_over_time, calculate_goal_percentage, Constants

st.set_page_config(
    page_title="NFT Weingarten - Player Performance",
)

st.title("Player Performance Analysis")
st.markdown(
        """
        This page allows you to compare the performance of multiple players over time,
        visualizing their goals, saves, and shots out.
        """
    )
data = load_data()
data[Constants.DATE_COL] = pd.to_datetime(data[Constants.DATE_COL]).dt.date

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

st.subheader("Compare Player Performance Over Time")
player_names = data[Constants.SHOOTER_NAME_COL].unique()
selected_players = st.multiselect(
    f"Select up to {Constants.MAX_PLAYER_SELECTIONS} Players to Compare",
    player_names,
    default=player_names[:int(Constants.MAX_PLAYER_SELECTIONS/2)],
    max_selections=Constants.MAX_PLAYER_SELECTIONS,
)

# Generate unique months for the dropdown
data['Month'] = pd.to_datetime(data[Constants.DATE_COL]).dt.to_period('M')
unique_months_period = sorted(data['Month'].unique(), reverse=True)
unique_months_display = [month.strftime("%B %Y") for month in unique_months_period]

selected_month_display = st.selectbox("Select a Month", unique_months_display)

# Determine start and end dates for the selected month
if selected_month_display:
    # Convert display format back to Period for date calculation
    selected_month_period = pd.Period(selected_month_display.replace(" ", "-"), freq='M')
    year = selected_month_period.year
    month = selected_month_period.month
    start_date_filter = pd.Timestamp(year=year, month=month, day=1).date()
    end_date_filter = (pd.Timestamp(year=year, month=month, day=1) + pd.DateOffset(months=1) - pd.Timedelta(days=1)).date()

    if selected_players:
        st.subheader(f"Performance Over Time")

        player_status_data = get_player_status_counts_over_time(data, selected_players, start_date=start_date_filter, end_date=end_date_filter)

        if not player_status_data.empty:
            # Aggregate data by player and status for the entire month
            monthly_player_status_summary = player_status_data.groupby([Constants.SHOOTER_NAME_COL, Constants.STATUS_COL])[Constants.COUNT_COL].sum().unstack(fill_value=0).reset_index()

            # Calculate total shots for each player in the month
            monthly_player_status_summary['Total Shots'] = monthly_player_status_summary[Constants.GOAL_STATUS] + monthly_player_status_summary[Constants.SAVED_STATUS] + monthly_player_status_summary[Constants.OUT_STATUS]

            # Calculate percentages for each status
            for status in [Constants.GOAL_STATUS, Constants.SAVED_STATUS, Constants.OUT_STATUS]:
                monthly_player_status_summary[status] = (monthly_player_status_summary[status] / monthly_player_status_summary['Total Shots']) * 100
                monthly_player_status_summary[status] = monthly_player_status_summary[status].fillna(0) # Handle division by zero if Total Shots is 0

            # Melt to long format for stacked bar chart
            player_outcome_percentages_melted = monthly_player_status_summary.melt(id_vars=[Constants.SHOOTER_NAME_COL, 'Total Shots'],
                                                                                value_vars=[Constants.GOAL_STATUS, Constants.SAVED_STATUS, Constants.OUT_STATUS],
                                                                                var_name=Constants.STATUS_COL, value_name='Percentage')

            # Filter out rows where Percentage is NaN (e.g., if Total Shots was 0)
            player_outcome_percentages_melted = player_outcome_percentages_melted.dropna(subset=['Percentage'])

            if not player_outcome_percentages_melted.empty:
                fig_total_outcome = px.bar(player_outcome_percentages_melted, x=Constants.SHOOTER_NAME_COL, y='Percentage',
                                           color=Constants.STATUS_COL,
                                           title=f"Outcome Distribution per Player in {selected_month_display}",
                                           category_orders={Constants.STATUS_COL: [Constants.GOAL_STATUS, Constants.SAVED_STATUS, Constants.OUT_STATUS]})
                fig_total_outcome.update_layout(yaxis_title="Percentage (%)", yaxis_range=[0, 100])
                st.plotly_chart(fig_total_outcome, use_container_width=True)
            else:
                st.info(f"No total outcome data to display for {', '.join(selected_players)} in {selected_month_display}.")
