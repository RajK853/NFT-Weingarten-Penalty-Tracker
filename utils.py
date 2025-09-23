import streamlit as st
import pandas as pd
from pathlib import Path
from typing import Optional, List, Tuple, Dict
from datetime import date
import plotly.graph_objects as go

class Constants:
    """
    A class to store all constant values used throughout the Streamlit application.
    This includes column names, status types, UI paths, and other magic numbers.
    """
    # Column Names
    DATE_COL: str = "Date"
    SHOOTER_NAME_COL: str = "Shooter Name"
    KEEPER_NAME_COL: str = "Keeper Name"
    STATUS_COL: str = "Status"
    REMARK_COL: str = "Remark"
    GOALS_COL: str = "Goals"
    MISSES_COL: str = "Misses"
    TOTAL_SHOTS_COL: str = "Total Shots"
    ADJUSTED_GOAL_PERCENTAGE_COL: str = "Adjusted Goal Percentage"
    GOAL_PERCENTAGE_COL: str = "Goal Percentage"
    COUNT_COL: str = "Count"
    SAVE_PERCENTAGE_COL: str = "Save Percentage"
    TOTAL_SAVES_COL: str = "Total Saves"
    TOTAL_FACED_COL: str = "Total Faced"

    # Trend Analysis Columns
    MONTH_COL: str = "Month"
    TOTAL_SHOTS_TREND_COL: str = "Total Shots"
    GOALS_TREND_COL: str = "Goals"
    SAVED_TREND_COL: str = "Saved"
    OUT_TREND_COL: str = "Out"
    GOAL_PERCENTAGE_TREND_COL: str = "Goal Percentage"
    SAVED_PERCENTAGE_TREND_COL: str = "Saved Percentage"
    OUT_PERCENTAGE_TREND_COL: str = "Out Percentage"
    OUTCOME_TYPE_COL: str = "Outcome Type"
    PERCENTAGE_COL: str = "Percentage"

    # Statuses
    GOAL_STATUS: str = "goal"
    SAVED_STATUS: str = "saved"
    OUT_STATUS: str = "out"

    # UI
    LOGO_PATH: str = "data/logo.jpg"
    LOGO_WIDTH: int = 100
    
    MAX_PLAYER_SELECTIONS: int = 10
    SCATTER_POINT_SIZE: int = 4

    # Goal Post Visual
    GOAL_WIDTH: int = 400
    GOAL_HEIGHT: int = 300
    GOAL_POST_LINE_WIDTH: int = 10
    GOAL_POST_COLOR: str = "white"
    PITCH_COLOR: str = "lightgreen"
    GRID_DIMENSION: int = 3 # For 3x3 grid
    GRID_LINES: int = 10
    GRID_SQUARE_SIZE: int = 20

    # Home Page UI
    PIE_CHART_PULL_EFFECT: float = 0.05
    Y_AXIS_RANGE_MIN: int = 0
    Y_AXIS_RANGE_MAX: int = 100
    RECENT_DAYS_FILTER: int = 30
    PERIOD_TYPE_DAYS: str = "Days"

    # Player Performance UI
    DEFAULT_NUM_PLAYERS_DISPLAY: int = 10
    DEFAULT_PLAYER_SELECTION_DIVISOR: int = 2
    PIE_CHART_HOLE_SIZE: float = 0.4

    # Goalkeeper Analysis UI
    TOP_N_KEEPERS_DISPLAY: int = 5

    # Shot Distribution UI
    SLIDER_MIN_MONTHS: int = 1
    SLIDER_MAX_MONTHS: int = 12
    SLIDER_DEFAULT_MONTHS: int = 12
    DECIMAL_POINTS_DISPLAY: int = 0
    GOAL_POST_WIDTH_VISUAL: int = 500
    GOAL_POST_HEIGHT_VISUAL: int = 400
    POST_LINE_WIDTH_VISUAL: int = 50
    FONT_SIZE_BASE: int = 12
    FONT_SIZE_SCALE: int = 20
    COLOR_MIN_RGB: int = 50
    COLOR_MAX_RGB: int = 200
    MARKER_SIZE_BASE: int = 5
    MARKER_SIZE_SCALE: int = 350
    X_POS_OFFSET: float = 0.5
    Y_POS_INVERT_FACTOR: float = 2.3

    # Pseudo Data Generation
    MIN_DAYS_PER_WEEK: int = 3
    MAX_DAYS_PER_WEEK: int = 4
    PSEUDO_DATA_OUTPUT_PATH: str = "data/pseudo_penalty.csv"


def load_data() -> pd.DataFrame:
    """
    Loads penalty shootout data from a CSV file.
    It first tries to load 'data/penalty.csv'. If not found, it falls back to 'data/pseudo_penalty.csv'.
    If neither is found, it displays an error and returns an empty DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the penalty shootout data.
    """
    real_data_path = Path("data/penalty.csv")
    pseudo_data_path = Path("data/pseudo_penalty.csv")

    if real_data_path.exists():
        data = pd.read_csv(real_data_path)
    elif pseudo_data_path.exists():
        st.warning("Real data (data/penalty.csv) not found. Loading pseudo data (data/pseudo_penalty.csv) instead.")
        data = pd.read_csv(pseudo_data_path)
    else:
        st.error("Neither real data nor pseudo data found. Please generate pseudo data or provide real data.")
        data = pd.DataFrame() # Return empty DataFrame if no data is found
    return data

@st.cache_data
def get_overall_statistics(data: pd.DataFrame, num_periods: Optional[int] = None, period_type: str = "Days") -> Tuple[int, float, pd.DataFrame]:
    """
    Calculates overall penalty shootout statistics, including total penalties, overall goal percentage,
    and outcome distribution.

    Args:
        data (pd.DataFrame): The input DataFrame containing penalty shootout data.
        num_periods (Optional[int]): If provided, filters data for the most recent N periods (Days, Months, Years).
        period_type (str): The type of period to filter by ("Days", "Months", "Years"). Defaults to "Days".

    Returns:
        Tuple[int, float, pd.DataFrame]: A tuple containing:
            - total_penalties (int): The total number of penalties.
            - overall_goal_percentage (float): The overall goal percentage.
            - outcome_distribution (pd.DataFrame): A DataFrame with the distribution of outcomes (goal, saved, out).
    """
    df = data.copy()

    if num_periods is not None:
        df[Constants.DATE_COL] = pd.to_datetime(df[Constants.DATE_COL])
        latest_date = df[Constants.DATE_COL].max()
        if period_type == "Days":
            start_date = latest_date - pd.DateOffset(days=num_periods)
        elif period_type == "Months":
            start_date = latest_date - pd.DateOffset(months=num_periods)
        elif period_type == "Years":
            start_date = latest_date - pd.DateOffset(years=num_periods)
        else:
            raise ValueError("period_type must be 'Days', 'Months', or 'Years'")
        df = df[df[Constants.DATE_COL] >= start_date]

    total_penalties = len(df)
    goals = len(df[df[Constants.STATUS_COL] == Constants.GOAL_STATUS])
    
    overall_goal_percentage = (goals / total_penalties) * 100 if total_penalties > 0 else 0

    outcome_distribution: pd.DataFrame = df[Constants.STATUS_COL].value_counts().reset_index() # type: ignore
    outcome_distribution.columns = [Constants.STATUS_COL, Constants.GOAL_PERCENTAGE_COL]

    return total_penalties, overall_goal_percentage, outcome_distribution

@st.cache_data
def calculate_goal_percentage(data: pd.DataFrame, num_months: Optional[int] = None) -> pd.DataFrame:
    """
    Calculates the goal percentage for each shooter using a Bayesian average.

    Args:
        data (pd.DataFrame): The input DataFrame containing penalty shootout data.
        num_months (Optional[int]): If provided, filters data for the most recent N months.

    Returns:
        pd.DataFrame: A DataFrame with shooter names, goals, misses, total shots, and adjusted goal percentage,
                      sorted by adjusted goal percentage in descending order.
    """
    df = data.copy()
    if num_months is not None:
        df[Constants.DATE_COL] = pd.to_datetime(df[Constants.DATE_COL])
        latest_date = df[Constants.DATE_COL].max()
        start_date = latest_date - pd.DateOffset(months=num_months)
        df = df[df[Constants.DATE_COL] >= start_date]

    goals = df[df[Constants.STATUS_COL] == Constants.GOAL_STATUS].groupby(Constants.SHOOTER_NAME_COL).size()
    misses = df[df[Constants.STATUS_COL] != Constants.GOAL_STATUS].groupby(Constants.SHOOTER_NAME_COL).size()
    
    ratio_df = pd.DataFrame({
        Constants.GOALS_COL: goals,
        Constants.MISSES_COL: misses
    }).fillna(0)
    
    ratio_df[Constants.MISSES_COL] = ratio_df[Constants.MISSES_COL].astype(int)
    ratio_df[Constants.TOTAL_SHOTS_COL] = ratio_df[Constants.GOALS_COL] + ratio_df[Constants.MISSES_COL]
    ratio_df[Constants.GOAL_PERCENTAGE_COL] = (ratio_df[Constants.GOALS_COL] / ratio_df[Constants.TOTAL_SHOTS_COL]) * 100
    ratio_df[Constants.GOAL_PERCENTAGE_COL] = ratio_df[Constants.GOAL_PERCENTAGE_COL].fillna(0) # Handle division by zero

    # Bayesian average calculation
    C = ratio_df[Constants.TOTAL_SHOTS_COL].mean()
    m = ratio_df[Constants.GOAL_PERCENTAGE_COL].mean()

    ratio_df[Constants.ADJUSTED_GOAL_PERCENTAGE_COL] = (ratio_df[Constants.GOAL_PERCENTAGE_COL] * ratio_df[Constants.TOTAL_SHOTS_COL] + m * C) / (ratio_df[Constants.TOTAL_SHOTS_COL] + C)
    
    return ratio_df.sort_values(by=Constants.ADJUSTED_GOAL_PERCENTAGE_COL, ascending=False)



@st.cache_data
def get_player_status_counts_over_time(data: pd.DataFrame, selected_players: List[str], start_date: Optional[date] = None, end_date: Optional[date] = None) -> pd.DataFrame:
    """
    Calculates the status counts (goals, saved, out) for selected players over a specified time period.

    Args:
        data (pd.DataFrame): The input DataFrame containing penalty shootout data.
        selected_players (List[str]): A list of player names to analyze.
        start_date (Optional[date]): The start date for filtering the data.
        end_date (Optional[date]): The end date for filtering the data.

    Returns:
        pd.DataFrame: A DataFrame with status counts for each player per day, ensuring all statuses are present.
    """
    if not selected_players:
        return pd.DataFrame() # Return empty DataFrame if no players selected

    filtered_data = data[data[Constants.SHOOTER_NAME_COL].isin(selected_players)].copy()
    filtered_data[Constants.DATE_COL] = pd.to_datetime(filtered_data[Constants.DATE_COL]).dt.date

    if start_date and end_date:
        filtered_data = filtered_data[(filtered_data[Constants.DATE_COL] >= start_date) & (filtered_data[Constants.DATE_COL] <= end_date)]

    # Count occurrences of each status for each player per day
    status_counts = filtered_data.groupby([Constants.DATE_COL, Constants.SHOOTER_NAME_COL, Constants.STATUS_COL]).size().reset_index(name=Constants.COUNT_COL)

    # Ensure all statuses are present for each date and player for consistent plotting
    all_dates = filtered_data[Constants.DATE_COL].unique()
    all_statuses = [Constants.GOAL_STATUS, Constants.SAVED_STATUS, Constants.OUT_STATUS]
    
    # Create a complete grid of all combinations
    idx = pd.MultiIndex.from_product([all_dates, selected_players, all_statuses], names=[Constants.DATE_COL, Constants.SHOOTER_NAME_COL, Constants.STATUS_COL])
    full_df = pd.DataFrame(index=idx).reset_index()

    # Merge with actual counts, filling missing with 0
    status_counts_full = pd.merge(full_df, status_counts, on=[Constants.DATE_COL, Constants.SHOOTER_NAME_COL, Constants.STATUS_COL], how="left").fillna(0)
    status_counts_full[Constants.COUNT_COL] = status_counts_full[Constants.COUNT_COL].astype(int)

    return status_counts_full.sort_values(by=[Constants.DATE_COL, Constants.SHOOTER_NAME_COL, Constants.STATUS_COL])


@st.cache_data
def calculate_save_percentage(data: pd.DataFrame, start_date: Optional[date] = None, end_date: Optional[date] = None) -> pd.DataFrame:
    """
    Calculates the save percentage for each goalkeeper within a specified date range.

    Args:
        data (pd.DataFrame): The input DataFrame containing penalty shootout data.
        start_date (Optional[date]): The start date for filtering the data.
        end_date (Optional[date]): The end date for filtering the data.

    Returns:
        pd.DataFrame: A DataFrame with goalkeeper names, total penalties faced, total saves, and save percentage,
                      sorted by save percentage in descending order.
    """
    df = data.copy()
    df[Constants.DATE_COL] = pd.to_datetime(df[Constants.DATE_COL])

    if start_date and end_date:
        df = df[(df[Constants.DATE_COL] >= pd.Timestamp(start_date)) & (df[Constants.DATE_COL] <= pd.Timestamp(end_date))]

    # Penalties faced by each keeper
    penalties_faced = df.groupby(Constants.KEEPER_NAME_COL).size()

    # Saves by each keeper
    saves = df[df[Constants.STATUS_COL] == Constants.SAVED_STATUS].groupby(Constants.KEEPER_NAME_COL).size()

    # Create a DataFrame for save percentages
    keeper_stats = pd.DataFrame({
        Constants.TOTAL_FACED_COL: penalties_faced,
        Constants.TOTAL_SAVES_COL: saves
    }).fillna(0)

    keeper_stats[Constants.TOTAL_SAVES_COL] = keeper_stats[Constants.TOTAL_SAVES_COL].astype(int)
    keeper_stats[Constants.SAVE_PERCENTAGE_COL] = (keeper_stats[Constants.TOTAL_SAVES_COL] / keeper_stats[Constants.TOTAL_FACED_COL]) * 100
    keeper_stats[Constants.SAVE_PERCENTAGE_COL] = keeper_stats[Constants.SAVE_PERCENTAGE_COL].fillna(0) # Handle division by zero

    return keeper_stats.sort_values(by=Constants.SAVE_PERCENTAGE_COL, ascending=False)




@st.cache_data
def get_overall_trend_data(data: pd.DataFrame, start_date: Optional[date] = None, end_date: Optional[date] = None) -> pd.DataFrame:
    """
    Calculates monthly trends for total shots, goals, saves, and outs, along with their percentages.

    Args:
        data (pd.DataFrame): The input DataFrame containing penalty shootout data.
        start_date (Optional[date]): The start date for filtering the data.
        end_date (Optional[date]): The end date for filtering the data.

    Returns:
        pd.DataFrame: A melted DataFrame suitable for plotting, showing monthly percentages of goals, saves, and outs.
    """
    df = data.copy()
    df[Constants.DATE_COL] = pd.to_datetime(df[Constants.DATE_COL]) # Convert to pd.Timestamp here

    if start_date and end_date:
        # Compare pd.Timestamp with datetime.date objects directly
        df = df[(df[Constants.DATE_COL] >= pd.Timestamp(start_date)) & (df[Constants.DATE_COL] <= pd.Timestamp(end_date))]

    df[Constants.MONTH_COL] = df[Constants.DATE_COL].dt.to_period('M')

    monthly_stats = df.groupby(Constants.MONTH_COL).apply(lambda x:
        pd.Series({
            Constants.TOTAL_SHOTS_TREND_COL: len(x),
            Constants.GOALS_TREND_COL: len(x[x[Constants.STATUS_COL] == Constants.GOAL_STATUS]),
            Constants.SAVED_TREND_COL: len(x[x[Constants.STATUS_COL] == Constants.SAVED_STATUS]),
            Constants.OUT_TREND_COL: len(x[x[Constants.STATUS_COL] == Constants.OUT_STATUS])
        }), include_groups=False # type: ignore
    ).reset_index()

    monthly_stats[Constants.GOAL_PERCENTAGE_TREND_COL] = (monthly_stats[Constants.GOALS_TREND_COL] / monthly_stats[Constants.TOTAL_SHOTS_TREND_COL]) * 100
    monthly_stats[Constants.SAVED_PERCENTAGE_TREND_COL] = (monthly_stats[Constants.SAVED_TREND_COL] / monthly_stats[Constants.TOTAL_SHOTS_TREND_COL]) * 100
    monthly_stats[Constants.OUT_PERCENTAGE_TREND_COL] = (monthly_stats[Constants.OUT_TREND_COL] / monthly_stats[Constants.TOTAL_SHOTS_TREND_COL]) * 100

    monthly_stats = monthly_stats.fillna(0)
    monthly_stats[Constants.MONTH_COL] = monthly_stats[Constants.MONTH_COL].astype(str)

    # Melt the DataFrame to long format for Plotly Express
    monthly_stats_melted = monthly_stats.melt(id_vars=[Constants.MONTH_COL, Constants.TOTAL_SHOTS_TREND_COL], 
                                              value_vars=[Constants.GOAL_PERCENTAGE_TREND_COL, Constants.SAVED_PERCENTAGE_TREND_COL, Constants.OUT_PERCENTAGE_TREND_COL],
                                              var_name=Constants.OUTCOME_TYPE_COL, value_name=Constants.PERCENTAGE_COL)

    return monthly_stats_melted

@st.cache_data
def get_monthly_outcome_distribution(data: pd.DataFrame, start_date: Optional[date] = None, end_date: Optional[date] = None) -> pd.DataFrame:
    """
    Calculates the monthly distribution of penalty outcomes (goal, saved, out) as percentages.

    Args:
        data (pd.DataFrame): The input DataFrame containing penalty shootout data.
        start_date (Optional[date]): The start date for filtering the data.
        end_date (Optional[date]): The end date for filtering the data.

    Returns:
        pd.DataFrame: A melted DataFrame showing monthly percentages for each outcome type.
    """
    df = data.copy()
    df[Constants.DATE_COL] = pd.to_datetime(df[Constants.DATE_COL])

    if start_date and end_date:
        df = df[(df[Constants.DATE_COL] >= pd.Timestamp(start_date)) & (df[Constants.DATE_COL] <= pd.Timestamp(end_date))]

    df[Constants.MONTH_COL] = df[Constants.DATE_COL].dt.to_period('M').astype(str)

    monthly_outcome_counts = df.groupby([Constants.MONTH_COL, Constants.STATUS_COL]).size().unstack(fill_value=0)
    monthly_outcome_percentages = monthly_outcome_counts.apply(lambda x: x / x.sum() * 100, axis=1)
    monthly_outcome_percentages = monthly_outcome_percentages.reset_index()

    # Melt the DataFrame to long format for Plotly Express
    monthly_outcome_percentages_melted = monthly_outcome_percentages.melt(id_vars=[Constants.MONTH_COL], var_name=Constants.STATUS_COL, value_name=Constants.GOAL_PERCENTAGE_COL)

    return monthly_outcome_percentages_melted

@st.cache_data
def get_keeper_outcome_distribution(data: pd.DataFrame, keeper_name: str, start_date: Optional[date] = None, end_date: Optional[date] = None) -> pd.DataFrame:
    """
    Calculates the distribution of outcomes (goals conceded, saves, outs) for a specific goalkeeper.

    Args:
        data (pd.DataFrame): The input DataFrame containing penalty shootout data.
        keeper_name (str): The name of the goalkeeper.
        start_date (Optional[date]): The start date for filtering the data.
        end_date (Optional[date]): The end date for filtering the data.

    Returns:
        pd.DataFrame: A DataFrame with outcome statuses and their counts and percentages for the given goalkeeper.
    """
    keeper_data = data[data[Constants.KEEPER_NAME_COL] == keeper_name].copy()
    keeper_data[Constants.DATE_COL] = pd.to_datetime(keeper_data[Constants.DATE_COL])

    if start_date and end_date:
        keeper_data = keeper_data[(keeper_data[Constants.DATE_COL] >= pd.Timestamp(start_date)) & (keeper_data[Constants.DATE_COL] <= pd.Timestamp(end_date))]
    
    # Count goals conceded (status == 'goal'), saves (status == 'saved'), and outs (status == 'out')
    goals_conceded = len(keeper_data[keeper_data[Constants.STATUS_COL] == Constants.GOAL_STATUS])
    saves = len(keeper_data[keeper_data[Constants.STATUS_COL] == Constants.SAVED_STATUS])
    outs = len(keeper_data[keeper_data[Constants.STATUS_COL] == Constants.OUT_STATUS])

    total_faced = goals_conceded + saves + outs

    if total_faced == 0:
        return pd.DataFrame(columns=[Constants.STATUS_COL, Constants.COUNT_COL])

    outcome_counts = pd.DataFrame({
        Constants.STATUS_COL: [Constants.GOAL_STATUS, Constants.SAVED_STATUS, Constants.OUT_STATUS],
        Constants.COUNT_COL: [goals_conceded, saves, outs]
    })
    
    # Calculate percentages for the pie chart
    outcome_counts[Constants.GOAL_PERCENTAGE_COL] = (outcome_counts[Constants.COUNT_COL] / total_faced) * 100

    return outcome_counts




