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
