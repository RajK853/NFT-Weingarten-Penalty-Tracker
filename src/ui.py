import time
import streamlit as st
from typing import Generator, Iterable, Any
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

def gender_selection_ui():
    """
    Creates a gender selection UI in the sidebar and returns the selected gender.
    Manages state across pages using st.session_state.
    """
    st.sidebar.title("Team Selection")

    gender_map = {
        Gender.MALE: f"👨 {Gender.MALE}",
        Gender.FEMALE: f"👩 {Gender.FEMALE}"
    }

    # Initialize the main gender state if it doesn't exist
    if SessionState.GENDER not in st.session_state:
        st.session_state[SessionState.GENDER] = Gender.MALE

    # Use a separate key for the widget itself
    selected_gender = st.sidebar.pills(
        "Gender",
        options=list(gender_map.keys()),
        format_func=lambda option: gender_map[option],
        key="gender_selector_widget", # A unique key for this specific widget instance
        default=st.session_state[SessionState.GENDER] # Explicitly set default from our main state
    )

    # On each run, update our main state variable with the current value of the widget
    st.session_state[SessionState.GENDER] = selected_gender

    return st.session_state[SessionState.GENDER]
