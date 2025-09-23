"""
Streamlit page for analyzing goalkeeper performance in penalties.
"""
import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data, calculate_save_percentage, get_keeper_outcome_distribution, Constants, _get_date_range_from_month_display
from typing import List, Optional
from datetime import date

st.set_page_config(
    page_title="NFT Weingarten - Goalkeeper Analysis",
    page_icon=Constants.EMOJI_GOALKEEPER_PAGE,
)

st.title("Goalkeeper Performance Analysis")
st.markdown(
        """
        This page offers a comprehensive analysis of goalkeeper performance in penalty shootouts. 
        Explore key metrics such as save percentages and detailed outcome distributions 
        to understand how different goalkeepers perform under pressure.
        """
    )

data: pd.DataFrame = load_data()
data[Constants.DATE_COL] = pd.to_datetime(data[Constants.DATE_COL]).dt.date

st.subheader("Goalkeeper Performance Analysis")
st.markdown("Utilize the month selector to analyze goalkeeper performance over specific periods. This section provides insights into their overall effectiveness in saving penalties and the distribution of outcomes they face.")

# Generate unique months for the dropdown
data[Constants.MONTH_COL] = pd.to_datetime(data[Constants.DATE_COL]).dt.to_period('M')
unique_months_period: List[pd.Period] = sorted(data[Constants.MONTH_COL].unique(), reverse=True)
unique_months_display: List[str] = [month.strftime("%B %Y") for month in unique_months_period]

selected_month_display: Optional[str] = st.selectbox("Select a Month for Goalkeeper Analysis", unique_months_display)

# Determine start and end dates for the selected month
if selected_month_display:
    start_date_filter, end_date_filter = _get_date_range_from_month_display(selected_month_display)

    keeper_performance_all: pd.DataFrame = calculate_save_percentage(data, start_date=start_date_filter, end_date=end_date_filter)

    top_n_keepers: List[str] = keeper_performance_all.head(Constants.TOP_N_KEEPERS_DISPLAY).index.tolist()

    # Create columns dynamically based on the number of top N goalkeepers
    cols = st.columns(len(top_n_keepers))

    for i, keeper in enumerate(top_n_keepers):
        with cols[i]:
            keeper_outcome_dist: pd.DataFrame = get_keeper_outcome_distribution(data, keeper, start_date=start_date_filter, end_date=end_date_filter)
            if not keeper_outcome_dist.empty:
                fig_keeper_outcome = px.pie(keeper_outcome_dist, values=Constants.COUNT_COL, names=Constants.STATUS_COL,
                                            title=keeper, hole=Constants.PIE_CHART_HOLE_SIZE)
                fig_keeper_outcome.update_traces(textinfo='percent+label', pull=[Constants.PIE_CHART_PULL_EFFECT if status == Constants.GOAL_STATUS else Constants.DEFAULT_FILL_VALUE for status in keeper_outcome_dist[Constants.STATUS_COL]])
                st.plotly_chart(fig_keeper_outcome, use_container_width=True, config={'displayModeBar': Constants.PLOTLY_DISPLAY_MODE_BAR})
            else:
                st.info(Constants.INFO_NO_KEEPER_DATA.format(keeper=keeper, selected_month_display=selected_month_display) + Constants.EMOJI_INFO_SAD)
else:
    st.info(Constants.INFO_SELECT_MONTH_KEEPER + Constants.EMOJI_INFO_CALENDAR)