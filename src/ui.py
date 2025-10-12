import time
from typing import Any, Generator, Iterable

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.constants import Columns, Data, Gender, Paths, SessionState, UI
from src.data_loader import load_data
def stream_data(
    iterable: Iterable[Any], timeout: float = Data.TYPING_ANIMATION_TIMEOUT
) -> Generator[Any, None, None]:
    """
    Streams an iterable with a delay between each item, simulating a typing effect.

    This function is designed to create a visual effect where data appears character by character
    or item by item, often used for displaying text output in a more engaging way.

    Args:
        iterable (Iterable[Any]): An iterable (e.g., a string, list of strings) to be streamed.
                                 Each item yielded by the iterable will be processed.
        timeout (float, optional): The delay in seconds after yielding each item.
                                 Defaults to `Data.TYPING_ANIMATION_TIMEOUT`.

    Yields:
        Generator[Any, None, None]: A generator that yields one item at a time from the iterable
                                    after the specified `timeout`.
    """
    for item in iterable:
        yield item
        time.sleep(timeout)


def gender_selection_ui() -> str:
    """
    Creates a gender selection UI widget in the Streamlit sidebar.

    This function displays a set of radio buttons (implemented as `st.pills`) in the sidebar
    allowing the user to select between 'Male' and 'Female' teams. The selection is stored
    and managed in `st.session_state` to persist across page reruns and different pages.

    Returns:
        str: The currently selected gender ('Male' or 'Female').
    """
    st.sidebar.subheader("Team Selection")
    st.sidebar.markdown("Filter data by team gender.")

    # Gender Selection
    gender_map = {
        Gender.MALE: f"👨 {Gender.MALE}",
        Gender.FEMALE: f"👩 {Gender.FEMALE}",
    }

    # Initialize the main gender state if it doesn't exist
    if SessionState.GENDER not in st.session_state:
        st.session_state[SessionState.GENDER] = Gender.MALE

    selected_gender = st.sidebar.pills(
        "Gender",
        options=list(gender_map.keys()),
        format_func=lambda option: gender_map[option],
        key="gender_selector_widget",
        default=st.session_state[SessionState.GENDER],
        width="stretch",
    )

    if selected_gender is None:
        selected_gender = Gender.MALE  # Default to male if None

    st.session_state[SessionState.GENDER] = selected_gender

    return st.session_state[SessionState.GENDER]


def data_refresh_button_ui() -> float:
    """
    Creates a data refresh button in the Streamlit sidebar.

    This function provides a button that, when clicked, updates a timestamp in `st.session_state`.
    This timestamp is then used by data loading functions (e.g., `load_data`) to trigger a reload
    of cached data, ensuring the application works with the latest information from external sources.
    A toast message confirms the data refresh.

    Returns:
        float: The Unix timestamp of the last data refresh. This value is primarily used
               as a cache-busting mechanism for `@st.cache_data` decorated functions.
    """
    st.sidebar.markdown("--- ")  # Add a separator
    st.sidebar.subheader("Data Update")
    st.sidebar.markdown("Update the lastest data from the Google Sheet.")

    # Data Refresh
    if "last_refresh_time" not in st.session_state:
        st.session_state.last_refresh_time = time.time()

    if st.sidebar.button(
        "Fetch Latest Data", use_container_width=True
    ):  # Changed button label for clarity
        st.session_state.last_refresh_time = time.time()
        st.toast("✅ Latest data loaded from Google Sheet!")  # Add toast message
        st.rerun()

    return st.session_state.last_refresh_time


import pandas as pd
from src.data_loader import load_data
from src.constants import Columns

def load_and_process_data() -> pd.DataFrame:
    """
    Handles gender selection, data refresh, data loading, and date conversion.

    Returns:
        pd.DataFrame: The processed DataFrame with the 'DATE' column converted to datetime objects.
    """
    gender_selection = gender_selection_ui()
    last_refresh_time = data_refresh_button_ui()
    st.info("You can change the gender from the left sidebar option.")
    st.markdown("---")

    data = load_data(gender=gender_selection, last_refresh_time=last_refresh_time)
    if not data.empty:
        data[Columns.DATE] = pd.to_datetime(data[Columns.DATE]).dt.date
    return data


def setup_page(
    page_title: str,
    page_icon: str,
    page_description: str,
    initial_sidebar_state: str = "expanded",
    layout: str = "wide",
):
    """
    Sets up the Streamlit page configuration and displays a standardized page header.

    This function combines `st.set_page_config` and `display_page_header` to ensure
    consistent page setup across the application.

    Args:
        page_title (str): The main title of the page.
        page_icon (str): An emoji or short string representing an icon for the page.
        page_description (str): A brief textual description of the page's content or purpose.
        initial_sidebar_state (str): Initial state of the sidebar ("auto", "expanded", or "collapsed").
                                     Defaults to "expanded".
        layout (str): Layout of the page ("centered" or "wide"). Defaults to "wide".
    """
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        initial_sidebar_state=initial_sidebar_state,
        layout=layout,
    )
    display_page_header(page_title, page_icon, page_description)


def display_page_header(page_title: str, page_icon: str, page_description: str):
    """
    Displays a standardized page header including a logo, a centered title, and a description.

    This function sets up a consistent visual header for different pages within the Streamlit application.
    It uses Streamlit columns for layout and Markdown for styling the title.

    Args:
        page_title (str): The main title of the page, displayed prominently.
        page_icon (str): An emoji or short string representing an icon for the page (currently unused in implementation but kept for potential future use).
        page_description (str): A brief textual description of the page's content or purpose.
    """
    col1, col2, col3 = st.columns([1, 0.3, 1])
    with col2:
        st.image(Paths.LOGO, width="stretch")

    st.markdown(
        f"<h1 style='text-align: center;'>{page_title}</h1>", unsafe_allow_html=True
    )

    st.markdown(
        f"""
    {page_description}
    """
    )
    st.write("")
    st.markdown("---")


def render_plotly_chart(
    fig: go.Figure, use_container_width: bool = True, hide_mode_bar: bool = True, fixed_range: bool = True
):
    """
    Renders a Plotly figure within a Streamlit application with common configurations.

    This function standardizes the display of Plotly charts, applying settings such as
    disabling zooming/panning and optionally hiding the mode bar. It ensures charts
    are responsive by default to the container width.

    Args:
        fig (go.Figure): The Plotly figure object to be rendered.
        use_container_width (bool): If True, the chart will expand to use the full width
                                    of its container. Defaults to True.
        hide_mode_bar (bool): If True, the Plotly mode bar (which includes tools like zoom,
                              pan, download) will be hidden. Defaults to True.
        fixed_range (bool): If True, disables zooming/panning on both x and y axes. Defaults to True.
    """
    # Apply fixedrange to axes to disable zooming/panning (general requirement)
    if fixed_range:
        fig.update_layout(xaxis_fixedrange=True, yaxis_fixedrange=True)

    # Configure st.plotly_chart
    config = {}
    if hide_mode_bar:
        config["displayModeBar"] = UI.PLOTLY_DISPLAY_MODE_BAR

    st.plotly_chart(fig, use_container_width=use_container_width, config=config)

def _calculate_y_axis_range(y_data: pd.Series, buffer_factor: float) -> tuple[float, float]:
    """
    Calculates the y-axis range with a buffer to prevent text truncation.

    Args:
        y_data (pd.Series): The data used for the y-axis.
        buffer_factor (float): The buffer factor to apply to the y-axis range.

    Returns:
        tuple[float, float]: A tuple containing the minimum and maximum y-axis values.
    """
    min_val = y_data.min()
    max_val = y_data.max()
    buffer = (max_val - min_val) * buffer_factor
    y_range_min = min_val - buffer
    y_range_max = max_val + buffer
    return y_range_min, y_range_max


def _update_plotly_layout(
    fig: go.Figure,
    y_range: tuple[float, float],
    yaxis_title: str = None,
    xaxis_title: str = None,
    margin_b: int = 200,
):
    """
    Updates the layout of a Plotly figure with the given y-axis range, titles, and margin.

    Args:
        fig (go.Figure): The Plotly figure object to be configured.
        y_range (tuple[float, float]): A tuple containing the minimum and maximum y-axis values.
        yaxis_title (str, optional): Title for the y-axis. Defaults to None.
        xaxis_title (str, optional): Title for the x-axis. Defaults to None.
        margin_b (int, optional): Bottom margin for the plot. Defaults to 200.
    """
    layout_updates = {
        "margin": dict(b=margin_b),
        "yaxis": dict(range=y_range),
    }
    if yaxis_title:
        layout_updates["yaxis_title"] = yaxis_title
    if xaxis_title:
        layout_updates["xaxis_title"] = xaxis_title

    fig.update_layout(**layout_updates)


def configure_plotly_layout(
    fig: go.Figure,
    y_data: pd.Series,
    yaxis_title: str = None,
    xaxis_title: str = None,
    margin_b: int = 200,
):
    """
    Configures common Plotly layout settings for bar charts, including y-axis range adjustment and margins.

    Args:
        fig (go.Figure): The Plotly figure object to be configured.
        y_data (pd.Series): The data used for the y-axis to calculate min/max for range adjustment.
        yaxis_title (str, optional): Title for the y-axis. Defaults to None.
        xaxis_title (str, optional): Title for the x-axis. Defaults to None.
        margin_b (int, optional): Bottom margin for the plot. Defaults to 200.
    """
    y_range = _calculate_y_axis_range(y_data, UI.CHART_Y_AXIS_BUFFER)
    _update_plotly_layout(fig, y_range, yaxis_title, xaxis_title, margin_b)
