import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data, calculate_save_percentage, get_keeper_outcome_distribution, Constants

st.set_page_config(
    page_title="NFT Weingarten - Goalkeeper Analysis",
)

st.title("Goalkeeper Performance Analysis")
st.markdown(
        """
        This page provides insights into goalkeeper performance, showing save percentages and outcome distributions for individual goalkeepers.
        """
    )

data = load_data()
data[Constants.DATE_COL] = pd.to_datetime(data[Constants.DATE_COL]).dt.date

st.subheader("Goalkeeper Performance Analysis")

# Generate unique months for the dropdown
data['Month'] = pd.to_datetime(data[Constants.DATE_COL]).dt.to_period('M')
unique_months_period = sorted(data['Month'].unique(), reverse=True)
unique_months_display = [month.strftime("%B %Y") for month in unique_months_period]

selected_month_display = st.selectbox("Select a Month for Goalkeeper Analysis", unique_months_display)

# Determine start and end dates for the selected month
if selected_month_display:
    selected_month_period = pd.Period(selected_month_display.replace(" ", "-"), freq='M')
    year = selected_month_period.year
    month = selected_month_period.month
    start_date_filter = pd.Timestamp(year=year, month=month, day=1).date()
    end_date_filter = (pd.Timestamp(year=year, month=month, day=1) + pd.DateOffset(months=1) - pd.Timedelta(days=1)).date()

    keeper_performance_all = calculate_save_percentage(data, start_date=start_date_filter, end_date=end_date_filter)
    top_5_keepers = keeper_performance_all.head(5).index.tolist()

    # Create columns dynamically based on the number of top 5 goalkeepers
    cols = st.columns(len(top_5_keepers))

    for i, keeper in enumerate(top_5_keepers):
        with cols[i]:
            keeper_outcome_dist = get_keeper_outcome_distribution(data, keeper, start_date=start_date_filter, end_date=end_date_filter)
            if not keeper_outcome_dist.empty:
                fig_keeper_outcome = px.pie(keeper_outcome_dist, values=Constants.COUNT_COL, names=Constants.STATUS_COL,
                                            title=keeper, hole=0.4)
                fig_keeper_outcome.update_traces(textinfo='percent+label', pull=[0.05 if s == Constants.GOAL_STATUS else 0 for s in keeper_outcome_dist[Constants.STATUS_COL]])
                st.plotly_chart(fig_keeper_outcome, use_container_width=True)
            else:
                st.info(f"No data available for {keeper} in {selected_month_display}.")
else:
    st.info("Please select a month to view goalkeeper performance.")
