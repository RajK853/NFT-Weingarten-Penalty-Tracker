import pandas as pd
import streamlit as st
from src.constants import Paths, Gender

@st.cache_data
def load_data(gender: str) -> pd.DataFrame:
    """
    Loads penalty shootout data for the specified gender.

    For males, it loads from a Google Sheet. For females, it loads from a local CSV.

    Args:
        gender (str): The gender to load data for ('Male' or 'Female').

    Returns:
        pd.DataFrame: A DataFrame containing the penalty shootout data.
    """
    with st.spinner(f"Loading {gender.lower()} team data..."):
        sheet_url: str = Paths.GOOGLE_SHEET_URL_MALE if gender == Gender.MALE else Paths.GOOGLE_SHEET_URL_FEMALE
        try:
            data = pd.read_csv(sheet_url)
            if data.empty:
                raise ValueError("Loaded data is empty.")
            
            st.success(f"Successfully loaded {gender.lower()} team data from Google Sheet.")
        except Exception as e:
            st.error(f"Failed to load data from Google Sheet: {e}")
            data = pd.read_csv(Paths.DATA_PSEUDO)
    return data
