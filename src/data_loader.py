import pandas as pd
import streamlit as st
from src.constants import Paths, Gender

@st.cache_data
def load_data(gender: str, last_refresh_time: float) -> pd.DataFrame:
    """
    Loads penalty shootout data for the specified gender.

    For males, it attempts to load data from a Google Sheet. If that fails or returns empty data,
    it falls back to loading from a local pseudo CSV file. For females, it always loads from
    the local pseudo CSV file as per project specifications.

    Args:
        gender (str): The gender to load data for ('Male' or 'Female').
        last_refresh_time (float): A timestamp used to bust the Streamlit cache.
                                   When this value changes, the data will be reloaded.

    Returns:
        pd.DataFrame: A DataFrame containing the penalty shootout data.
                      Includes error handling and fallback to local pseudo data if Google Sheet loading fails.
    """
    with st.spinner(f"Loading {gender.lower()} team data..."):
        if gender == Gender.MALE:
            sheet_url: str = Paths.GOOGLE_SHEET_URL_MALE
            try:
                data = pd.read_csv(sheet_url)
                if data.empty:
                    raise ValueError("Loaded data is empty.")
                
                st.success(f"Successfully loaded {gender.lower()} team data from Google Sheet.")
            except Exception as e:
                st.error(f"Failed to load data from Google Sheet: {e}")
                data = pd.read_csv(Paths.DATA_PSEUDO)
        else: # gender == Gender.FEMALE
            data = pd.read_csv(Paths.DATA_PSEUDO)
            st.info(f"Loading {gender.lower()} team data from local pseudo data as per project specification.")
    return data
