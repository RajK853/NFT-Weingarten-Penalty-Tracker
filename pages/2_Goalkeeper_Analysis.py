"""
Streamlit page for analyzing goalkeeper performance in penalties.
"""

from datetime import date
from typing import List, Optional

import pandas as pd
import plotly.express as px
import streamlit as st

from src.analysis import (
    _get_date_range_from_month_display,
    calculate_keeper_scores,
    get_keeper_outcome_distribution,
)
from src.constants import Columns, Data, Scoring, Status, UI
from src.data_loader import load_data
from src.ui import (
    data_refresh_button_ui,
    display_page_header,
    gender_selection_ui,
    render_plotly_chart,
)

st.set_page_config(
    page_title="NFT Weingarten - Goalkeeper Analysis",
    page_icon=UI.EMOJI_GOALKEEPER_PAGE,
    initial_sidebar_state="expanded",
    layout="wide",
)

# --- Header ---

display_page_header(
    page_title="Goalkeeper Performance Analysis",
    page_icon=UI.EMOJI_GOALKEEPER_PAGE,
    page_description="""
    This page analyzes goalkeeper performance. 
    You can see scores and how many goals were saved or missed.
    """,
)

gender_selection = gender_selection_ui()
last_refresh_time = data_refresh_button_ui()
data: pd.DataFrame = load_data(
    gender=gender_selection, last_refresh_time=last_refresh_time
)
data[Columns.DATE] = pd.to_datetime(data[Columns.DATE]).dt.date

with st.container(border=True):
    st.subheader("Goalkeeper Performance Analysis")
    st.markdown(
        "Use the month selector to see how goalkeepers performed in a specific month. You can see how good they are at saving penalties."
    )
    st.info(
        f"Rankings use a time-weighted score to show who is in good form now. The current half-life is {Scoring.PERFORMANCE_HALF_LIFE_DAYS} days."
    )

    # Generate unique months for the dropdown
    data[Columns.MONTH] = pd.to_datetime(data[Columns.DATE]).dt.to_period("M")
    unique_months_period: List[pd.Period] = sorted(
        data[Columns.MONTH].unique(), reverse=True
    )
    unique_months_display: List[str] = [
        month.strftime("%B %Y") for month in unique_months_period
    ]

    selected_month_display: Optional[str] = st.selectbox(
        "Select a Month for Goalkeeper Analysis", unique_months_display
    )

    # Determine start and end dates for the selected month
    if selected_month_display:
        start_date_filter, end_date_filter = _get_date_range_from_month_display(
            selected_month_display
        )

        keeper_performance_all: pd.DataFrame = calculate_keeper_scores(
            data, start_date=start_date_filter, end_date=end_date_filter
        )

        top_n_keepers: List[str] = keeper_performance_all.head(
            UI.TOP_N_KEEPERS_DISPLAY
        ).index.tolist()

        # Create columns dynamically based on the number of top N goalkeepers
        cols = st.columns(len(top_n_keepers))

        for i, keeper in enumerate(top_n_keepers):
            with cols[i]:
                keeper_score = keeper_performance_all.loc[keeper][Columns.SCORE]
                st.metric(label=f"{keeper}", value=f"{keeper_score:.2f} pts")
                keeper_outcome_dist: pd.DataFrame = get_keeper_outcome_distribution(
                    data, keeper, start_date=start_date_filter, end_date=end_date_filter
                )
                if not keeper_outcome_dist.empty:
                    fig_keeper_outcome = px.pie(
                        keeper_outcome_dist,
                        values=Columns.COUNT,
                        names=Columns.STATUS,
                        title=f"Outcome Distribution for {keeper}",
                        hole=UI.PIE_CHART_HOLE_SIZE,
                    )
                    fig_keeper_outcome.update_traces(
                        textinfo="percent+label",
                        pull=[
                            (
                                UI.PIE_CHART_PULL_EFFECT
                                if status == Status.GOAL
                                else Data.DEFAULT_FILL_VALUE
                            )
                            for status in keeper_outcome_dist[Columns.STATUS]
                        ],
                    )
                    render_plotly_chart(fig_keeper_outcome)
                else:
                    st.info(
                        UI.INFO_NO_KEEPER_DATA.format(
                            keeper=keeper, selected_month_display=selected_month_display
                        )
                        + UI.EMOJI_INFO_SAD
                    )
    else:
        st.info(UI.INFO_SELECT_MONTH_KEEPER + UI.EMOJI_INFO_CALENDAR)
