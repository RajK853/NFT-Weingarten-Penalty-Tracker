import time
import streamlit as st
from typing import Generator, Iterable, Any
from src.constants import Data, Gender, SessionState, Paths, UI
import plotly.graph_objects as go

def stream_data(iterable: Iterable[Any], timeout: float = Data.TYPING_ANIMATION_TIMEOUT) -> Generator[Any, None, None]:
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
        Gender.FEMALE: f"👩 {Gender.FEMALE}"
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
        width="stretch"
    )

    if selected_gender is None:
        selected_gender = Gender.MALE # Default to male if None

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
    st.sidebar.markdown("--- ") # Add a separator
    st.sidebar.subheader("Data Update")
    st.sidebar.markdown("Update the lastest data from the Google Sheet.")

    # Data Refresh
    if "last_refresh_time" not in st.session_state:
        st.session_state.last_refresh_time = time.time()

    if st.sidebar.button("Fetch Latest Data", use_container_width=True): # Changed button label for clarity
        st.session_state.last_refresh_time = time.time()
        st.toast("✅ Latest data loaded from Google Sheet!") # Add toast message
        st.rerun()

    return st.session_state.last_refresh_time

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
    col1, col2, col3 = st.columns([1,0.3,1])
    with col2:
        st.image(Paths.LOGO, width='stretch')

    st.markdown(f"<h1 style='text-align: center;'>{page_title}</h1>", unsafe_allow_html=True)

    st.markdown(f"""
    {page_description}
    """)
    st.write("")
    st.markdown("---")

def render_plotly_chart(fig: go.Figure, use_container_width: bool = True, hide_mode_bar: bool = True):
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
    """
    # Apply fixedrange to axes to disable zooming/panning (general requirement)
    fig.update_layout(xaxis_fixedrange=True, yaxis_fixedrange=True)

    # Configure st.plotly_chart
    config = {}
    if hide_mode_bar:
        config['displayModeBar'] = UI.PLOTLY_DISPLAY_MODE_BAR

    st.plotly_chart(fig, use_container_width=use_container_width, config=config)