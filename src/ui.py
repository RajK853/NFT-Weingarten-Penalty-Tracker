import time
import streamlit as st
from typing import Generator, Iterable, Any, Tuple
from src.constants import Data, Gender, SessionState

def stream_data(iterable: Iterable[Any], timeout: float = Data.TYPING_ANIMATION_TIMEOUT) -> Generator[Any, None, None]:
    """
    Streams an iterable with a delay between each item.

    This function takes an iterable and yields each string from the
    iterable one by one. A delay, controlled by the `timeout` parameter, is
    introduced after each string is yielded.

    Args:
        iterable (Iterable[Any]): An iterable to be streamed.
        timeout (float, optional): The delay in seconds after yielding each string.
                                 Defaults to `Data.TYPING_ANIMATION_TIMEOUT`.

    Yields:
        Generator[Any, None, None]: A generator that yields one item at a time from the iterable.
    """
    for item in iterable:
        yield item
        time.sleep(timeout)

def gender_selection_ui() -> str:
    """
    Creates a gender selection UI in the sidebar and returns the selected gender.
    Manages state across pages using st.session_state.
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
    Creates a data refresh button UI in the sidebar and returns the last refresh time.
    Manages state across pages using st.session_state.
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