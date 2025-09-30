import time
from pathlib import Path
from datetime import date
from typing import Optional, List, Tuple, Generator, Iterable, Any

import pandas as pd
import streamlit as st
import plotly.graph_objects as go


class Constants:
    """
    A class to store all constant values used throughout the Streamlit application.
    This includes column names, status types, UI paths, and other magic numbers.
    """
    class Columns:
        DATE: str = "Date"
        SHOOTER_NAME: str = "Shooter Name"
        KEEPER_NAME: str = "Keeper Name"
        STATUS: str = "Status"
        REMARK: str = "Remark"
        GOALS: str = "Goals"
        MISSES: str = "Misses"
        TOTAL_SHOTS: str = "Total Shots"
        SCORE: str = "Score"
        GOAL_PERCENTAGE: str = "Goal Percentage"
        COUNT: str = "Count"
        SAVE_PERCENTAGE: str = "Save Percentage"
        TOTAL_SAVES: str = "Total Saves"
        TOTAL_FACED: str = "Total Faced"
        SHOT_X: str = "Shot_X"
        SHOT_Y: str = "Shot_Y"
        MONTH: str = "Month"
        TOTAL_SHOTS_TREND: str = "Total Shots"
        GOALS_TREND: str = "Goals"
        SAVED_TREND: str = "Saved"
        OUT_TREND: str = "Out"
        GOAL_PERCENTAGE_TREND: str = "Goal Percentage"
        SAVED_PERCENTAGE_TREND: str = "Saved Percentage"
        OUT_PERCENTAGE_TREND: str = "Out Percentage"
        OUTCOME_TYPE: str = "Outcome Type"
        PERCENTAGE: str = "Percentage"

    class Status:
        GOAL: str = "goal"
        SAVED: str = "saved"
        OUT: str = "out"

    class Scoring:
        GOAL: float = +1.5
        SAVED: float = 0.0
        OUT: float = -1.0

    class Paths:
        LOGO: str = "data/logo.jpg"
        DATA_PSEUDO: str = "data/pseudo_penalty.csv"
        GOOGLE_SHEET_URL_MALE: str = "https://docs.google.com/spreadsheets/d/1ehIA2Ea_8wCMy5ICmwFl14FZUPLA8ki6VQBLcGqsVUU/gviz/tq?tqx=out:csv&sheet=RawData"
        GOOGLE_SHEET_URL_FEMALE: str = "https://docs.google.com/spreadsheets/d/1WdCk7X4HUnJKfaVxnDDtOZ_06l_kSxni22w9kXyQ6yE/gviz/tq?tqx=out:csv&sheet=RawData"
        
    class Gender:
        MALE: str = "Male"
        FEMALE: str = "Female"

    class SessionState:
        GENDER: str = "gender"

    class UI:
        LOGO_WIDTH: int = 150
        EMOJI_HOME_PAGE: str = "🏠"
        HOME_PAGE_COLUMN_RATIO: List[int] = [1, 4]
        MAX_PLAYER_SELECTIONS: int = 10
        SCATTER_POINT_SIZE: int = 4
        MAX_NAMES_IN_METRIC_DISPLAY: int = 3
        PIE_CHART_PULL_EFFECT: float = 0.05
        Y_AXIS_RANGE_MIN: int = 0
        Y_AXIS_RANGE_MAX: int = 100
        RECENT_DAYS_FILTER: int = 365
        PERIOD_TYPE_DAYS: str = "Days"
        PERIOD_TYPE_MONTHS: str = "Months"
        GOLD_TEXT_STYLE: str = "color: gold; text-shadow: 0 0 2px gold, 0 0 4px gold, 0 0 6px gold;"
        TOP_N_PLAYERS_LEADERBOARD: int = 10
        DEFAULT_NUM_PLAYERS_MULTISELECT: int = 4
        PIE_CHART_HOLE_SIZE: float = 0.4
        CHART_Y_AXIS_BUFFER: float = 0.1
        COLOR_GREEN: str = "green"
        COLOR_RED: str = "red"
        COLOR_LIGHTGRAY: str = "lightgray"
        COLOR_BLUE: str = "blue"
        PLOTLY_DISPLAY_MODE_BAR: bool = False
        PLOTLY_FIXED_RANGE: bool = True
        PLOTLY_TEXT_TEMPLATE: str = '%{y}'
        PLOTLY_TEXT_POSITION_OUTSIDE: str = 'outside'
        PLOTLY_SCATTER_MARKER_SIZE: int = 10
        PLOTLY_SCATTER_MARKER_OPACITY: float = 0.7
        PLOTLY_BG_COLOR_TRANSPARENT: str = 'rgba(0,0,0,0)'
        PLOTLY_SHOW_LEGEND: bool = True
        PLOTLY_AXIS_SHOWGRID: bool = False
        PLOTLY_AXIS_ZEROLINE: bool = False
        PLOTLY_AXIS_VISIBLE: bool = False
        EMOJI_PLAYER_PAGE: str = "⚽"
        EMOJI_GOALKEEPER_PAGE: str = "🧤"
        EMOJI_INFO_SAD: str = "😔"
        EMOJI_INFO_CALENDAR: str = "🗓️"
        INFO_SELECT_DATE_RANGE: str = "Please select both a start and end date for the leaderboard."
        INFO_NO_PLAYER_DATA: str = "No data available for the selected players in {selected_month_display}. Please select different players or a different month. 😔"
        INFO_NO_KEEPER_DATA: str = "No data available for {keeper} in {selected_month_display}. 😔"
        INFO_SELECT_MONTH_KEEPER: str = "Please select a month to view goalkeeper performance. 🗓️"
        TAB_SCORE: str = "Score"
        TAB_GOALS: str = "Goals"
        TAB_SAVED: str = "Saved"
        TAB_OUT: str = "Out"
        TAB_OUTCOME_DISTRIBUTION: str = "Outcome Distribution"
        TOP_N_KEEPERS_DISPLAY: int = 5
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

    class Data:
        PERCENTAGE_MULTIPLIER: int = 100
        DEFAULT_FILL_VALUE: int = 0
        DATE_OFFSET_MONTHS_ONE: int = 1
        DATE_OFFSET_DAYS_ONE: int = 1
        DATE_DAY_ONE: int = 1
        TYPING_ANIMATION_TIMEOUT: float = 0.2
        MIN_DAYS_PER_WEEK: int = 3
        MAX_DAYS_PER_WEEK: int = 4
        PSEUDO_DATA_OUTPUT_PATH: str = "data/pseudo_penalty.csv"

    class GoalVisual:
        GOAL_WIDTH: int = 400
        GOAL_HEIGHT: int = 300
        GOAL_POST_LINE_WIDTH: int = 10
        GOAL_POST_COLOR: str = "white"
        PITCH_COLOR: str = "lightgreen"
        GRID_DIMENSION: int = 3 # For 3x3 grid
        GRID_LINES: int = 10
        GRID_SQUARE_SIZE: int = 20


def stream_data(iterable: Iterable[Any], timeout: float = Constants.Data.TYPING_ANIMATION_TIMEOUT) -> Generator[Any, None, None]:
    """
    Streams an iterable with a delay between each item.

    This function takes an iterable and yields each string from the
    iterable one by one. A delay, controlled by the `timeout` parameter, is
    introduced after each string is yielded.

    Args:
        iterable (Iterable[Any]): An iterable to be streamed.
        timeout (float, optional): The delay in seconds after yielding each string.
                                 Defaults to `Constants.TYPING_ANIMATION_TIMEOUT`.

    Yields:
        Generator[Any, None, None]: A generator that yields one item at a time from the iterable.
    """
    for item in iterable:
        yield item
        time.sleep(timeout)

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
        sheet_url: str = Constants.Paths.GOOGLE_SHEET_URL_MALE if gender == Constants.Gender.MALE else Constants.Paths.GOOGLE_SHEET_URL_FEMALE
        try:
            data = pd.read_csv(sheet_url)
            if data.empty:
                raise ValueError("Loaded data is empty.")
            
            st.success(f"Successfully loaded {gender.lower()} team data from Google Sheet.")
        except Exception as e:
            st.error(f"Failed to load data from Google Sheet: {e}")
            data = pd.read_csv(Constants.Paths.DATA_PSEUDO)
    return data

def _get_date_range_from_month_display(selected_month_display: str) -> Tuple[date, date]:
    """
    Helper function to determine the start and end dates for a given month display string.
    """
    selected_month_period: pd.Period = pd.Period(selected_month_display.replace(" ", "-"), freq='M')
    year: int = selected_month_period.year
    month: int = selected_month_period.month
    start_date_filter: date = pd.Timestamp(year=year, month=month, day=Constants.Data.DATE_DAY_ONE).date()
    end_date_filter: date = (pd.Timestamp(year=year, month=month, day=Constants.Data.DATE_DAY_ONE) + pd.DateOffset(months=Constants.Data.DATE_OFFSET_MONTHS_ONE) - pd.Timedelta(days=Constants.Data.DATE_OFFSET_DAYS_ONE)).date()
    return start_date_filter, end_date_filter

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
    with st.spinner("Calculating overall statistics..."):
        df = data.copy()

        if num_periods is not None:
            df[Constants.Columns.DATE] = pd.to_datetime(df[Constants.Columns.DATE])
            latest_date = df[Constants.Columns.DATE].max()
            if period_type == "Days":
                start_date = latest_date - pd.DateOffset(days=num_periods)
            elif period_type == "Months":
                start_date = latest_date - pd.DateOffset(months=num_periods)
            elif period_type == "Years":
                start_date = latest_date - pd.DateOffset(years=num_periods)
            else:
                raise ValueError("period_type must be 'Days', 'Months', or 'Years'")
            df = df[df[Constants.Columns.DATE] >= start_date]

        total_penalties = len(df)
        goals = len(df[df[Constants.Columns.STATUS] == Constants.Status.GOAL])
        
        overall_goal_percentage = (goals / total_penalties) * Constants.Data.PERCENTAGE_MULTIPLIER if total_penalties > Constants.Data.DEFAULT_FILL_VALUE else Constants.Data.DEFAULT_FILL_VALUE

        outcome_distribution: pd.DataFrame = df[Constants.Columns.STATUS].value_counts().reset_index() # type: ignore
        outcome_distribution.columns = [Constants.Columns.STATUS, Constants.Columns.GOAL_PERCENTAGE]

        return total_penalties, overall_goal_percentage, outcome_distribution

@st.cache_data
def calculate_player_scores(data: pd.DataFrame, start_date: Optional[date] = None, end_date: Optional[date] = None) -> pd.DataFrame:
    """
    Calculates the total score for each shooter based on the outcome of their shots.

    Args:
        data (pd.DataFrame): The input DataFrame containing penalty shootout data.
        start_date (Optional[date]): The start date for filtering the data.
        end_date (Optional[date]): The end date for filtering the data.

    Returns:
        pd.DataFrame: A DataFrame with shooter names and their total scores,
                      sorted by score in descending order.
    """
    with st.spinner("Calculating player scores..."):
        df = data.copy()
        df[Constants.Columns.DATE] = pd.to_datetime(df[Constants.Columns.DATE])

        if start_date and end_date:
            df = df[(df[Constants.Columns.DATE] >= pd.Timestamp(start_date)) & (df[Constants.Columns.DATE] <= pd.Timestamp(end_date))]

        goals = df[df[Constants.Columns.STATUS] == Constants.Status.GOAL].groupby(Constants.Columns.SHOOTER_NAME).size().fillna(0)
        saved = df[df[Constants.Columns.STATUS] == Constants.Status.SAVED].groupby(Constants.Columns.SHOOTER_NAME).size().fillna(0)
        out = df[df[Constants.Columns.STATUS] == Constants.Status.OUT].groupby(Constants.Columns.SHOOTER_NAME).size().fillna(0)

        score_df = pd.DataFrame({
            Constants.Status.GOAL : goals,
            Constants.Status.SAVED: saved,
            Constants.Status.OUT  : out,
        }).fillna(Constants.Data.DEFAULT_FILL_VALUE)

        score_df[Constants.Columns.SCORE] = (score_df[Constants.Status.GOAL] * Constants.Scoring.GOAL) + (score_df[Constants.Status.SAVED] * Constants.Scoring.SAVED) + (score_df[Constants.Status.OUT] * Constants.Scoring.OUT)

        return score_df.sort_values(by=Constants.Columns.SCORE, ascending=False)


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
    with st.spinner("Calculating player status counts..."):
        if not selected_players:
            return pd.DataFrame() # Return empty DataFrame if no players selected

        filtered_data = data[data[Constants.Columns.SHOOTER_NAME].isin(selected_players)].copy()
        filtered_data[Constants.Columns.DATE] = pd.to_datetime(filtered_data[Constants.Columns.DATE]).dt.date

        if start_date and end_date:
            filtered_data = filtered_data[(filtered_data[Constants.Columns.DATE] >= start_date) & (filtered_data[Constants.Columns.DATE] <= end_date)]

        # Count occurrences of each status for each player per day
        status_counts = filtered_data.groupby([Constants.Columns.DATE, Constants.Columns.SHOOTER_NAME, Constants.Columns.STATUS]).size().reset_index(name=Constants.Columns.COUNT)

        # Ensure all statuses are present for each date and player for consistent plotting
        all_dates = filtered_data[Constants.Columns.DATE].unique()
        all_statuses = [Constants.Status.GOAL, Constants.Status.SAVED, Constants.Status.OUT]
        
        # Create a complete grid of all combinations
        idx = pd.MultiIndex.from_product([all_dates, selected_players, all_statuses], names=[Constants.Columns.DATE, Constants.Columns.SHOOTER_NAME, Constants.Columns.STATUS])
        full_df = pd.DataFrame(index=idx).reset_index()

        # Merge with actual counts, filling missing with 0
        status_counts_full = pd.merge(full_df, status_counts, on=[Constants.Columns.DATE, Constants.Columns.SHOOTER_NAME, Constants.Columns.STATUS], how="left").fillna(Constants.Data.DEFAULT_FILL_VALUE)
        status_counts_full[Constants.Columns.COUNT] = status_counts_full[Constants.Columns.COUNT].astype(int)

        return status_counts_full.sort_values(by=[Constants.Columns.DATE, Constants.Columns.SHOOTER_NAME, Constants.Columns.STATUS])


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
    with st.spinner("Calculating save percentages..."):
        df = data.copy()
        df[Constants.Columns.DATE] = pd.to_datetime(df[Constants.Columns.DATE])

        if start_date and end_date:
            df = df[(df[Constants.Columns.DATE] >= pd.Timestamp(start_date)) & (df[Constants.Columns.DATE] <= pd.Timestamp(end_date))]

        # Penalties faced by each keeper
        penalties_faced = df.groupby(Constants.Columns.KEEPER_NAME).size()

        # Saves by each keeper
        saves = df[df[Constants.Columns.STATUS] == Constants.Status.SAVED].groupby(Constants.Columns.KEEPER_NAME).size()

        # Create a DataFrame for save percentages
        keeper_stats = pd.DataFrame({
            Constants.Columns.TOTAL_FACED: penalties_faced,
            Constants.Columns.TOTAL_SAVES: saves
        }).fillna(Constants.Data.DEFAULT_FILL_VALUE)

        keeper_stats[Constants.Columns.TOTAL_SAVES] = keeper_stats[Constants.Columns.TOTAL_SAVES].astype(int)
        keeper_stats[Constants.Columns.SAVE_PERCENTAGE] = (keeper_stats[Constants.Columns.TOTAL_SAVES] / keeper_stats[Constants.Columns.TOTAL_FACED]) * Constants.Data.PERCENTAGE_MULTIPLIER
        keeper_stats[Constants.Columns.SAVE_PERCENTAGE] = keeper_stats[Constants.Columns.SAVE_PERCENTAGE].fillna(Constants.Data.DEFAULT_FILL_VALUE) # Handle division by zero

        return keeper_stats.sort_values(by=Constants.Columns.SAVE_PERCENTAGE, ascending=False)




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
    with st.spinner("Calculating overall trend data..."):
        df = data.copy()
        df[Constants.Columns.DATE] = pd.to_datetime(df[Constants.Columns.DATE]) # Convert to pd.Timestamp here

        if start_date and end_date:
            # Compare pd.Timestamp with datetime.date objects directly
            df = df[(df[Constants.Columns.DATE] >= pd.Timestamp(start_date)) & (df[Constants.Columns.DATE] <= pd.Timestamp(end_date))]

        df[Constants.Columns.MONTH] = df[Constants.Columns.DATE].dt.to_period('M')

        monthly_stats = df.groupby(Constants.Columns.MONTH).apply(lambda x:
            pd.Series({
                Constants.Columns.TOTAL_SHOTS_TREND: len(x),
                Constants.Columns.GOALS_TREND: len(x[x[Constants.Columns.STATUS] == Constants.Status.GOAL]),
                Constants.Columns.SAVED_TREND: len(x[x[Constants.Columns.STATUS] == Constants.Status.SAVED]),
                Constants.Columns.OUT_TREND: len(x[x[Constants.Columns.STATUS] == Constants.Status.OUT])
            }), include_groups=False # type: ignore
        ).reset_index()

        monthly_stats[Constants.Columns.GOAL_PERCENTAGE_TREND] = (monthly_stats[Constants.Columns.GOALS_TREND] / monthly_stats[Constants.Columns.TOTAL_SHOTS_TREND]) * Constants.Data.PERCENTAGE_MULTIPLIER
        monthly_stats[Constants.Columns.SAVED_PERCENTAGE_TREND] = (monthly_stats[Constants.Columns.SAVED_TREND] / monthly_stats[Constants.Columns.TOTAL_SHOTS_TREND]) * Constants.Data.PERCENTAGE_MULTIPLIER
        monthly_stats[Constants.Columns.OUT_PERCENTAGE_TREND] = (monthly_stats[Constants.Columns.OUT_TREND] / monthly_stats[Constants.Columns.TOTAL_SHOTS_TREND]) * Constants.Data.PERCENTAGE_MULTIPLIER

        monthly_stats = monthly_stats.fillna(Constants.Data.DEFAULT_FILL_VALUE)
        monthly_stats[Constants.Columns.MONTH] = monthly_stats[Constants.Columns.MONTH].astype(str)

        # Melt the DataFrame to long format for Plotly Express
        monthly_stats_melted = monthly_stats.melt(id_vars=[Constants.Columns.MONTH, Constants.Columns.TOTAL_SHOTS_TREND], 
                                                  value_vars=[Constants.Columns.GOAL_PERCENTAGE_TREND, Constants.Columns.SAVED_PERCENTAGE_TREND, Constants.Columns.OUT_PERCENTAGE_TREND],
                                                  var_name=Constants.Columns.OUTCOME_TYPE, value_name=Constants.Columns.PERCENTAGE)

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
    with st.spinner("Calculating monthly outcome distribution..."):
        df = data.copy()
        df[Constants.Columns.DATE] = pd.to_datetime(df[Constants.Columns.DATE])

        if start_date and end_date:
            df = df[(df[Constants.Columns.DATE] >= pd.Timestamp(start_date)) & (df[Constants.Columns.DATE] <= pd.Timestamp(end_date))]

        df[Constants.Columns.MONTH] = df[Constants.Columns.DATE].dt.to_period('M').astype(str)

        monthly_outcome_counts = df.groupby([Constants.Columns.MONTH, Constants.Columns.STATUS]).size().unstack(fill_value=Constants.Data.DEFAULT_FILL_VALUE)
        monthly_outcome_percentages = monthly_outcome_counts.apply(lambda x: x / x.sum() * Constants.Data.PERCENTAGE_MULTIPLIER, axis=1)
        monthly_outcome_percentages = monthly_outcome_percentages.reset_index()

        # Melt the DataFrame to long format for Plotly Express
        monthly_outcome_percentages_melted = monthly_outcome_percentages.melt(id_vars=[Constants.Columns.MONTH], var_name=Constants.Columns.STATUS, value_name=Constants.Columns.GOAL_PERCENTAGE)

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
    with st.spinner("Calculating keeper outcome distribution..."):
        keeper_data = data[data[Constants.Columns.KEEPER_NAME] == keeper_name].copy()
        keeper_data[Constants.Columns.DATE] = pd.to_datetime(keeper_data[Constants.Columns.DATE])

        if start_date and end_date:
            keeper_data = keeper_data[(keeper_data[Constants.Columns.DATE] >= pd.Timestamp(start_date)) & (keeper_data[Constants.Columns.DATE] <= pd.Timestamp(end_date))]
        
        # Count goals conceded (status == 'goal'), saves (status == 'saved'), and outs (status == 'out')
        goals_conceded = len(keeper_data[keeper_data[Constants.Columns.STATUS] == Constants.Status.GOAL])
        saves = len(keeper_data[keeper_data[Constants.Columns.STATUS] == Constants.Status.SAVED])
        outs = len(keeper_data[keeper_data[Constants.Columns.STATUS] == Constants.Status.OUT])

        total_faced = goals_conceded + saves + outs

        if total_faced == Constants.Data.DEFAULT_FILL_VALUE:
            return pd.DataFrame(columns=[Constants.Columns.STATUS, Constants.Columns.COUNT])

        outcome_counts = pd.DataFrame({
            Constants.Columns.STATUS: [Constants.Status.GOAL, Constants.Status.SAVED, Constants.Status.OUT],
            Constants.Columns.COUNT: [goals_conceded, saves, outs]
        })
        
        # Calculate percentages for the pie chart
        outcome_counts[Constants.Columns.GOAL_PERCENTAGE] = (outcome_counts[Constants.Columns.COUNT] / total_faced) * Constants.Data.PERCENTAGE_MULTIPLIER

        return outcome_counts


def create_shot_distribution_chart(data: pd.DataFrame) -> go.Figure:
    """
    Creates a scatter plot of shot distribution on a goalpost visual.

    Args:
        data (pd.DataFrame): The input DataFrame containing penalty shootout data
                             with 'Shot_X', 'Shot_Y', and 'Status' columns.

    Returns:
        go.Figure: A Plotly Graph Object figure displaying the shot distribution.
    """
    fig = go.Figure()

    # Draw the goalpost (simplified rectangle)
    fig.add_shape(
        type="rect",
        x0=0, y0=0, x1=Constants.GoalVisual.GOAL_WIDTH, y1=Constants.GoalVisual.GOAL_HEIGHT,
        line=dict(color=Constants.GoalVisual.GOAL_POST_COLOR, width=Constants.GoalVisual.GOAL_POST_LINE_WIDTH),
        fillcolor=Constants.GoalVisual.PITCH_COLOR
    )

    # Add scatter points for each shot
    # Assuming Shot_X and Shot_Y are normalized or within the GOAL_WIDTH/GOAL_HEIGHT range
    fig.add_trace(go.Scatter(
        x=data[Constants.Columns.SHOT_X],
        y=data[Constants.Columns.SHOT_Y],
        mode='markers',
        marker=dict(
            size=Constants.UI.PLOTLY_SCATTER_MARKER_SIZE,
            color=data[Constants.Columns.STATUS].map({
                Constants.Status.GOAL: Constants.UI.COLOR_GREEN,
                Constants.Status.SAVED: Constants.UI.COLOR_BLUE,
                Constants.Status.OUT: Constants.UI.COLOR_RED
            }),
            opacity=Constants.UI.PLOTLY_SCATTER_MARKER_OPACITY
        ),
        text=data.apply(lambda row: f"Shooter: {row[Constants.Columns.SHOOTER_NAME]}<br>Outcome: {row[Constants.Columns.STATUS]}", axis=1),
        hoverinfo='text'
    ))

    fig.update_layout(
        title="Shot Distribution on Goal",
        xaxis=dict(range=[Constants.Data.DEFAULT_FILL_VALUE, Constants.GoalVisual.GOAL_WIDTH], showgrid=Constants.UI.PLOTLY_AXIS_SHOWGRID, zeroline=Constants.UI.PLOTLY_AXIS_ZEROLINE, visible=Constants.UI.PLOTLY_AXIS_VISIBLE),
        yaxis=dict(range=[Constants.Data.DEFAULT_FILL_VALUE, Constants.GoalVisual.GOAL_HEIGHT], showgrid=Constants.UI.PLOTLY_AXIS_SHOWGRID, zeroline=Constants.UI.PLOTLY_AXIS_ZEROLINE, visible=Constants.UI.PLOTLY_AXIS_VISIBLE),
        plot_bgcolor=Constants.UI.PLOTLY_BG_COLOR_TRANSPARENT, # Make plot background transparent to show pitch color
        showlegend=Constants.UI.PLOTLY_SHOW_LEGEND,
        width=Constants.UI.GOAL_POST_WIDTH_VISUAL,
        height=Constants.UI.GOAL_POST_HEIGHT_VISUAL
    )

    return fig

@st.cache_data
def get_recent_penalties(data: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Returns the last n penalties."""
    return data.tail(n)

@st.cache_data
def get_longest_goal_streak(data: pd.DataFrame) -> Tuple[List[str], int]:
    """Calculates the longest goal streak and returns all players who achieved it."""
    longest_streak = 0
    streaking_players = []

    if data.empty or Constants.Columns.SHOOTER_NAME not in data.columns:
        return [], 0

    for player in data[Constants.Columns.SHOOTER_NAME].unique():
        player_data = data[data[Constants.Columns.SHOOTER_NAME] == player]
        current_streak = 0
        max_player_streak = 0
        
        for status in player_data[Constants.Columns.STATUS]:
            if status == Constants.Status.GOAL:
                current_streak += 1
            else:
                max_player_streak = max(current_streak, max_player_streak)
                current_streak = 0
        
        # Final check in case the streak is at the end
        max_player_streak = max(current_streak, max_player_streak)

        # Compare with the global longest streak
        if max_player_streak > longest_streak:
            longest_streak = max_player_streak
            streaking_players = [player]
        elif max_player_streak == longest_streak and longest_streak > 0:
            streaking_players.append(player)

    return streaking_players, longest_streak

@st.cache_data
def get_most_goals_in_session(data: pd.DataFrame) -> Tuple[str, date, int]:
    """Finds the player who scored the most goals in a single session."""
    goals_in_session = data[data[Constants.Columns.STATUS] == Constants.Status.GOAL].groupby([Constants.Columns.DATE, Constants.Columns.SHOOTER_NAME]).size().reset_index(name='goals')
    if not goals_in_session.empty:
        most_goals = goals_in_session.loc[goals_in_session['goals'].idxmax()]
        return most_goals[Constants.Columns.SHOOTER_NAME], most_goals[Constants.Columns.DATE], most_goals['goals']
    
    return None, None, 0

@st.cache_data
def get_marathon_man(data: pd.DataFrame) -> Tuple[List[str], int]:
    """Finds the player(s) who have participated in the most sessions."""
    if data.empty or Constants.Columns.SHOOTER_NAME not in data.columns:
        return [], 0

    session_counts = data.groupby(Constants.Columns.SHOOTER_NAME)[Constants.Columns.DATE].nunique()
    
    if session_counts.empty:
        return [], 0
        
    max_sessions = session_counts.max()
    
    if max_sessions == 0:
        return [], 0
        
    marathon_men = session_counts[session_counts == max_sessions].index.tolist()
    
    return marathon_men, int(max_sessions)

@st.cache_data
def get_mysterious_ninja(data: pd.DataFrame) -> Tuple[List[str], int]:
    """Finds the player(s) who have participated in the fewest sessions."""
    if data.empty or Constants.Columns.SHOOTER_NAME not in data.columns:
        return [], 0

    session_counts = data.groupby(Constants.Columns.SHOOTER_NAME)[Constants.Columns.DATE].nunique()
    
    if session_counts.empty:
        return [], 0
        
    min_sessions = session_counts.min()
    
    if min_sessions == 0:
        return [], 0
        
    mysterious_ninjas = session_counts[session_counts == min_sessions].index.tolist()
    
    return mysterious_ninjas, int(min_sessions)

@st.cache_data
def get_busiest_day(data: pd.DataFrame) -> Tuple[date, int]:
    """Finds the date with the most penalties taken."""
    day_counts = data.groupby(Constants.Columns.DATE).size()
    if not day_counts.empty:
        busiest_day = day_counts.idxmax()
        return busiest_day, day_counts.max()
    return None, 0

@st.cache_data
def get_biggest_rivalry(data: pd.DataFrame) -> Tuple[str, str, int]:
    """Finds the most frequent shooter-keeper matchup."""
    rivalry_counts = data.groupby([Constants.Columns.SHOOTER_NAME, Constants.Columns.KEEPER_NAME]).size().reset_index(name='encounters')
    if not rivalry_counts.empty:
        biggest_rivalry = rivalry_counts.loc[rivalry_counts['encounters'].idxmax()]
        return biggest_rivalry[Constants.Columns.SHOOTER_NAME], biggest_rivalry[Constants.Columns.KEEPER_NAME], biggest_rivalry['encounters']
    
    return None, None, 0

@st.cache_data
def get_most_saves_in_session(data: pd.DataFrame) -> Tuple[str, date, int]:
    """Finds the keeper who saved the most goals in a single session."""
    saves_in_session = data[data[Constants.Columns.STATUS] == Constants.Status.SAVED].groupby([Constants.Columns.DATE, Constants.Columns.KEEPER_NAME]).size().reset_index(name='saves')
    if not saves_in_session.empty:
        most_saves = saves_in_session.loc[saves_in_session['saves'].idxmax()]
        return most_saves[Constants.Columns.KEEPER_NAME], most_saves[Constants.Columns.DATE], most_saves['saves']
    
    return None, None, 0

def gender_selection_ui():
    """
    Creates a gender selection UI in the sidebar and returns the selected gender.
    Manages state across pages using st.session_state.
    """
    st.sidebar.title("Team Selection")

    gender_map = {
        Constants.Gender.MALE: f"👨 {Constants.Gender.MALE}",
        Constants.Gender.FEMALE: f"👩 {Constants.Gender.FEMALE}"
    }

    # Initialize the main gender state if it doesn't exist
    if Constants.SessionState.GENDER not in st.session_state:
        st.session_state[Constants.SessionState.GENDER] = Constants.Gender.MALE

    # Use a separate key for the widget itself
    selected_gender = st.sidebar.pills(
        "Gender",
        options=list(gender_map.keys()),
        format_func=lambda option: gender_map[option],
        key="gender_selector_widget", # A unique key for this specific widget instance
        default=st.session_state[Constants.SessionState.GENDER] # Explicitly set default from our main state
    )

    # On each run, update our main state variable with the current value of the widget
    st.session_state[Constants.SessionState.GENDER] = selected_gender

    return st.session_state[Constants.SessionState.GENDER]
