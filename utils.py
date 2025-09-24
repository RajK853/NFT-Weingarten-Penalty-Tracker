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
    SCORE_COL: str = "Score"
    GOAL_PERCENTAGE_COL: str = "Goal Percentage"
    COUNT_COL: str = "Count"
    SAVE_PERCENTAGE_COL: str = "Save Percentage"
    TOTAL_SAVES_COL: str = "Total Saves"
    TOTAL_FACED_COL: str = "Total Faced"
    SHOT_X_COL: str = "Shot_X"
    SHOT_Y_COL: str = "Shot_Y"

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

    # Scoring
    GOAL_SCORE: int = 1
    SAVED_SCORE: int = 0
    OUT_SCORE: int = -1

    # UI
    LOGO_PATH: str = "data/logo.jpg"
    LOGO_WIDTH: int = 100
    EMOJI_HOME_PAGE: str = "🏠"
    HOME_PAGE_COLUMN_RATIO: List[int] = [1, 4]
    
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
    PERIOD_TYPE_MONTHS: str = "Months"
    GOLD_TEXT_STYLE: str = "color: gold; text-shadow: 0 0 2px gold, 0 0 4px gold, 0 0 6px gold;"

    # Player Performance UI
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

    # Data Processing/Calculations
    PERCENTAGE_MULTIPLIER: int = 100
    DEFAULT_FILL_VALUE: int = 0
    DATE_OFFSET_MONTHS_ONE: int = 1
    DATE_OFFSET_DAYS_ONE: int = 1
    DATE_DAY_ONE: int = 1

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

    with st.spinner("Loading data..."):
        if real_data_path.exists():
            data = pd.read_csv(real_data_path)
        elif pseudo_data_path.exists():
            st.warning("Real data (data/penalty.csv) not found. Loading pseudo data (data/pseudo_penalty.csv) instead.")
            data = pd.read_csv(pseudo_data_path)
        else:
            st.error("No data found! Please generate pseudo data using `generate_pseudo_data.py` or provide real data. 📊")
            data = pd.DataFrame() # Return empty DataFrame if no data is found
    return data

def _get_date_range_from_month_display(selected_month_display: str) -> Tuple[date, date]:
    """
    Helper function to determine the start and end dates for a given month display string.
    """
    selected_month_period: pd.Period = pd.Period(selected_month_display.replace(" ", "-"), freq='M')
    year: int = selected_month_period.year
    month: int = selected_month_period.month
    start_date_filter: date = pd.Timestamp(year=year, month=month, day=Constants.DATE_DAY_ONE).date()
    end_date_filter: date = (pd.Timestamp(year=year, month=month, day=Constants.DATE_DAY_ONE) + pd.DateOffset(months=Constants.DATE_OFFSET_MONTHS_ONE) - pd.Timedelta(days=Constants.DATE_OFFSET_DAYS_ONE)).date()
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
        
        overall_goal_percentage = (goals / total_penalties) * Constants.PERCENTAGE_MULTIPLIER if total_penalties > Constants.DEFAULT_FILL_VALUE else Constants.DEFAULT_FILL_VALUE

        outcome_distribution: pd.DataFrame = df[Constants.STATUS_COL].value_counts().reset_index() # type: ignore
        outcome_distribution.columns = [Constants.STATUS_COL, Constants.GOAL_PERCENTAGE_COL]

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
        df[Constants.DATE_COL] = pd.to_datetime(df[Constants.DATE_COL])

        if start_date and end_date:
            df = df[(df[Constants.DATE_COL] >= pd.Timestamp(start_date)) & (df[Constants.DATE_COL] <= pd.Timestamp(end_date))]

        goals = df[df[Constants.STATUS_COL] == Constants.GOAL_STATUS].groupby(Constants.SHOOTER_NAME_COL).size().fillna(0)
        saved = df[df[Constants.STATUS_COL] == Constants.SAVED_STATUS].groupby(Constants.SHOOTER_NAME_COL).size().fillna(0)
        out = df[df[Constants.STATUS_COL] == Constants.OUT_STATUS].groupby(Constants.SHOOTER_NAME_COL).size().fillna(0)

        score_df = pd.DataFrame({
            Constants.GOAL_STATUS : goals,
            Constants.SAVED_STATUS: saved,
            Constants.OUT_STATUS  : out,
        }).fillna(Constants.DEFAULT_FILL_VALUE)

        score_df[Constants.SCORE_COL] = (score_df[Constants.GOAL_STATUS] * Constants.GOAL_SCORE) + (score_df[Constants.SAVED_STATUS] * Constants.SAVED_SCORE) + (score_df[Constants.OUT_STATUS] * Constants.OUT_SCORE)

        return score_df.sort_values(by=Constants.SCORE_COL, ascending=False)


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
        status_counts_full = pd.merge(full_df, status_counts, on=[Constants.DATE_COL, Constants.SHOOTER_NAME_COL, Constants.STATUS_COL], how="left").fillna(Constants.DEFAULT_FILL_VALUE)
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
    with st.spinner("Calculating save percentages..."):
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
        }).fillna(Constants.DEFAULT_FILL_VALUE)

        keeper_stats[Constants.TOTAL_SAVES_COL] = keeper_stats[Constants.TOTAL_SAVES_COL].astype(int)
        keeper_stats[Constants.SAVE_PERCENTAGE_COL] = (keeper_stats[Constants.TOTAL_SAVES_COL] / keeper_stats[Constants.TOTAL_FACED_COL]) * Constants.PERCENTAGE_MULTIPLIER
        keeper_stats[Constants.SAVE_PERCENTAGE_COL] = keeper_stats[Constants.SAVE_PERCENTAGE_COL].fillna(Constants.DEFAULT_FILL_VALUE) # Handle division by zero

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
    with st.spinner("Calculating overall trend data..."):
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

        monthly_stats[Constants.GOAL_PERCENTAGE_TREND_COL] = (monthly_stats[Constants.GOALS_TREND_COL] / monthly_stats[Constants.TOTAL_SHOTS_TREND_COL]) * Constants.PERCENTAGE_MULTIPLIER
        monthly_stats[Constants.SAVED_PERCENTAGE_TREND_COL] = (monthly_stats[Constants.SAVED_TREND_COL] / monthly_stats[Constants.TOTAL_SHOTS_TREND_COL]) * Constants.PERCENTAGE_MULTIPLIER
        monthly_stats[Constants.OUT_PERCENTAGE_TREND_COL] = (monthly_stats[Constants.OUT_TREND_COL] / monthly_stats[Constants.TOTAL_SHOTS_TREND_COL]) * Constants.PERCENTAGE_MULTIPLIER

        monthly_stats = monthly_stats.fillna(Constants.DEFAULT_FILL_VALUE)
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
    with st.spinner("Calculating monthly outcome distribution..."):
        df = data.copy()
        df[Constants.DATE_COL] = pd.to_datetime(df[Constants.DATE_COL])

        if start_date and end_date:
            df = df[(df[Constants.DATE_COL] >= pd.Timestamp(start_date)) & (df[Constants.DATE_COL] <= pd.Timestamp(end_date))]

        df[Constants.MONTH_COL] = df[Constants.DATE_COL].dt.to_period('M').astype(str)

        monthly_outcome_counts = df.groupby([Constants.MONTH_COL, Constants.STATUS_COL]).size().unstack(fill_value=Constants.DEFAULT_FILL_VALUE)
        monthly_outcome_percentages = monthly_outcome_counts.apply(lambda x: x / x.sum() * Constants.PERCENTAGE_MULTIPLIER, axis=1)
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
    with st.spinner("Calculating keeper outcome distribution..."):
        keeper_data = data[data[Constants.KEEPER_NAME_COL] == keeper_name].copy()
        keeper_data[Constants.DATE_COL] = pd.to_datetime(keeper_data[Constants.DATE_COL])

        if start_date and end_date:
            keeper_data = keeper_data[(keeper_data[Constants.DATE_COL] >= pd.Timestamp(start_date)) & (keeper_data[Constants.DATE_COL] <= pd.Timestamp(end_date))]
        
        # Count goals conceded (status == 'goal'), saves (status == 'saved'), and outs (status == 'out')
        goals_conceded = len(keeper_data[keeper_data[Constants.STATUS_COL] == Constants.GOAL_STATUS])
        saves = len(keeper_data[keeper_data[Constants.STATUS_COL] == Constants.SAVED_STATUS])
        outs = len(keeper_data[keeper_data[Constants.STATUS_COL] == Constants.OUT_STATUS])

        total_faced = goals_conceded + saves + outs

        if total_faced == Constants.DEFAULT_FILL_VALUE:
            return pd.DataFrame(columns=[Constants.STATUS_COL, Constants.COUNT_COL])

        outcome_counts = pd.DataFrame({
            Constants.STATUS_COL: [Constants.GOAL_STATUS, Constants.SAVED_STATUS, Constants.OUT_STATUS],
            Constants.COUNT_COL: [goals_conceded, saves, outs]
        })
        
        # Calculate percentages for the pie chart
        outcome_counts[Constants.GOAL_PERCENTAGE_COL] = (outcome_counts[Constants.COUNT_COL] / total_faced) * Constants.PERCENTAGE_MULTIPLIER

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
        x0=0, y0=0, x1=Constants.GOAL_WIDTH, y1=Constants.GOAL_HEIGHT,
        line=dict(color=Constants.GOAL_POST_COLOR, width=Constants.GOAL_POST_LINE_WIDTH),
        fillcolor=Constants.PITCH_COLOR
    )

    # Add scatter points for each shot
    # Assuming Shot_X and Shot_Y are normalized or within the GOAL_WIDTH/GOAL_HEIGHT range
    fig.add_trace(go.Scatter(
        x=data[Constants.SHOT_X_COL],
        y=data[Constants.SHOT_Y_COL],
        mode='markers',
        marker=dict(
            size=Constants.PLOTLY_SCATTER_MARKER_SIZE,
            color=data[Constants.STATUS_COL].map({
                Constants.GOAL_STATUS: Constants.COLOR_GREEN,
                Constants.SAVED_STATUS: Constants.COLOR_BLUE,
                Constants.OUT_STATUS: Constants.COLOR_RED
            }),
            opacity=Constants.PLOTLY_SCATTER_MARKER_OPACITY
        ),
        text=data.apply(lambda row: f"Shooter: {row[Constants.SHOOTER_NAME_COL]}<br>Outcome: {row[Constants.STATUS_COL]}", axis=1),
        hoverinfo='text'
    ))

    fig.update_layout(
        title="Shot Distribution on Goal",
        xaxis=dict(range=[Constants.DEFAULT_FILL_VALUE, Constants.GOAL_WIDTH], showgrid=Constants.PLOTLY_AXIS_SHOWGRID, zeroline=Constants.PLOTLY_AXIS_ZEROLINE, visible=Constants.PLOTLY_AXIS_VISIBLE),
        yaxis=dict(range=[Constants.DEFAULT_FILL_VALUE, Constants.GOAL_HEIGHT], showgrid=Constants.PLOTLY_AXIS_SHOWGRID, zeroline=Constants.PLOTLY_AXIS_ZEROLINE, visible=Constants.PLOTLY_AXIS_VISIBLE),
        plot_bgcolor=Constants.PLOTLY_BG_COLOR_TRANSPARENT, # Make plot background transparent to show pitch color
        showlegend=Constants.PLOTLY_SHOW_LEGEND,
        width=Constants.GOAL_POST_WIDTH_VISUAL,
        height=Constants.GOAL_POST_HEIGHT_VISUAL
    )

    return fig




