from datetime import date
from typing import Optional, List, Tuple
import pandas as pd
import streamlit as st
from src.constants import Columns, Data, Status, Scoring

def _get_date_range_from_month_display(selected_month_display: str) -> Tuple[date, date]:
    """
    Helper function to determine the start and end dates for a given month display string.
    """
    selected_month_period: pd.Period = pd.Period(selected_month_display.replace(" ", "-"), freq='M')
    year: int = selected_month_period.year
    month: int = selected_month_period.month
    start_date_filter: date = pd.Timestamp(year=year, month=month, day=Data.DATE_DAY_ONE).date()
    end_date_filter: date = (pd.Timestamp(year=year, month=month, day=Data.DATE_DAY_ONE) + pd.DateOffset(months=Data.DATE_OFFSET_MONTHS_ONE) - pd.Timedelta(days=Data.DATE_OFFSET_DAYS_ONE)).date()
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
            df[Columns.DATE] = pd.to_datetime(df[Columns.DATE])
            latest_date = df[Columns.DATE].max()
            if period_type == "Days":
                start_date = latest_date - pd.DateOffset(days=num_periods)
            elif period_type == "Months":
                start_date = latest_date - pd.DateOffset(months=num_periods)
            elif period_type == "Years":
                start_date = latest_date - pd.DateOffset(years=num_periods)
            else:
                raise ValueError("period_type must be 'Days', 'Months', or 'Years'")
            df = df[df[Columns.DATE] >= start_date]

        total_penalties = len(df)
        goals = len(df[df[Columns.STATUS] == Status.GOAL])
        
        overall_goal_percentage = (goals / total_penalties) * Data.PERCENTAGE_MULTIPLIER if total_penalties > Data.DEFAULT_FILL_VALUE else Data.DEFAULT_FILL_VALUE

        outcome_distribution: pd.DataFrame = df[Columns.STATUS].value_counts().reset_index() # type: ignore
        outcome_distribution.columns = [Columns.STATUS, Columns.GOAL_PERCENTAGE]

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
        df[Columns.DATE] = pd.to_datetime(df[Columns.DATE])

        if start_date and end_date:
            df = df[(df[Columns.DATE] >= pd.Timestamp(start_date)) & (df[Columns.DATE] <= pd.Timestamp(end_date))]

        goals = df[df[Columns.STATUS] == Status.GOAL].groupby(Columns.SHOOTER_NAME).size().fillna(0)
        saved = df[df[Columns.STATUS] == Status.SAVED].groupby(Columns.SHOOTER_NAME).size().fillna(0)
        out = df[df[Columns.STATUS] == Status.OUT].groupby(Columns.SHOOTER_NAME).size().fillna(0)

        score_df = pd.DataFrame({
            Status.GOAL : goals,
            Status.SAVED: saved,
            Status.OUT  : out,
        }).fillna(Data.DEFAULT_FILL_VALUE)

        score_df[Columns.SCORE] = (score_df[Status.GOAL] * Scoring.GOAL) + (score_df[Status.SAVED] * Scoring.SAVED) + (score_df[Status.OUT] * Scoring.OUT)

        return score_df.sort_values(by=Columns.SCORE, ascending=False)


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

        filtered_data = data[data[Columns.SHOOTER_NAME].isin(selected_players)].copy()
        filtered_data[Columns.DATE] = pd.to_datetime(filtered_data[Columns.DATE]).dt.date

        if start_date and end_date:
            filtered_data = filtered_data[(filtered_data[Columns.DATE] >= start_date) & (filtered_data[Columns.DATE] <= end_date)]

        # Count occurrences of each status for each player per day
        status_counts = filtered_data.groupby([Columns.DATE, Columns.SHOOTER_NAME, Columns.STATUS]).size().reset_index(name=Columns.COUNT)

        # Ensure all statuses are present for each date and player for consistent plotting
        all_dates = filtered_data[Columns.DATE].unique()
        all_statuses = [Status.GOAL, Status.SAVED, Status.OUT]
        
        # Create a complete grid of all combinations
        idx = pd.MultiIndex.from_product([all_dates, selected_players, all_statuses], names=[Columns.DATE, Columns.SHOOTER_NAME, Columns.STATUS])
        full_df = pd.DataFrame(index=idx).reset_index()

        # Merge with actual counts, filling missing with 0
        status_counts_full = pd.merge(full_df, status_counts, on=[Columns.DATE, Columns.SHOOTER_NAME, Columns.STATUS], how="left").fillna(Data.DEFAULT_FILL_VALUE)
        status_counts_full[Columns.COUNT] = status_counts_full[Columns.COUNT].astype(int)

        return status_counts_full.sort_values(by=[Columns.DATE, Columns.SHOOTER_NAME, Columns.STATUS])


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
        df[Columns.DATE] = pd.to_datetime(df[Columns.DATE])

        if start_date and end_date:
            df = df[(df[Columns.DATE] >= pd.Timestamp(start_date)) & (df[Columns.DATE] <= pd.Timestamp(end_date))]

        # Penalties faced by each keeper
        penalties_faced = df.groupby(Columns.KEEPER_NAME).size()

        # Saves by each keeper
        saves = df[df[Columns.STATUS] == Status.SAVED].groupby(Columns.KEEPER_NAME).size()

        # Create a DataFrame for save percentages
        keeper_stats = pd.DataFrame({
            Columns.TOTAL_FACED: penalties_faced,
            Columns.TOTAL_SAVES: saves
        }).fillna(Data.DEFAULT_FILL_VALUE)

        keeper_stats[Columns.TOTAL_SAVES] = keeper_stats[Columns.TOTAL_SAVES].astype(int)
        keeper_stats[Columns.SAVE_PERCENTAGE] = (keeper_stats[Columns.TOTAL_SAVES] / keeper_stats[Columns.TOTAL_FACED]) * Data.PERCENTAGE_MULTIPLIER
        keeper_stats[Columns.SAVE_PERCENTAGE] = keeper_stats[Columns.SAVE_PERCENTAGE].fillna(Data.DEFAULT_FILL_VALUE) # Handle division by zero

        return keeper_stats.sort_values(by=Columns.SAVE_PERCENTAGE, ascending=False)

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
        df[Columns.DATE] = pd.to_datetime(df[Columns.DATE]) # Convert to pd.Timestamp here

        if start_date and end_date:
            # Compare pd.Timestamp with datetime.date objects directly
            df = df[(df[Columns.DATE] >= pd.Timestamp(start_date)) & (df[Columns.DATE] <= pd.Timestamp(end_date))]

        df[Columns.MONTH] = df[Columns.DATE].dt.to_period('M')

        monthly_stats = df.groupby(Columns.MONTH).apply(lambda x:
            pd.Series({
                Columns.TOTAL_SHOTS_TREND: len(x),
                Columns.GOALS_TREND: len(x[x[Columns.STATUS] == Status.GOAL]),
                Columns.SAVED_TREND: len(x[x[Columns.STATUS] == Status.SAVED]),
                Columns.OUT_TREND: len(x[x[Columns.STATUS] == Status.OUT])
            }), include_groups=False # type: ignore
        ).reset_index()

        monthly_stats[Columns.GOAL_PERCENTAGE_TREND] = (monthly_stats[Columns.GOALS_TREND] / monthly_stats[Columns.TOTAL_SHOTS_TREND]) * Data.PERCENTAGE_MULTIPLIER
        monthly_stats[Columns.SAVED_PERCENTAGE_TREND] = (monthly_stats[Columns.SAVED_TREND] / monthly_stats[Columns.TOTAL_SHOTS_TREND]) * Data.PERCENTAGE_MULTIPLIER
        monthly_stats[Columns.OUT_PERCENTAGE_TREND] = (monthly_stats[Columns.OUT_TREND] / monthly_stats[Columns.TOTAL_SHOTS_TREND]) * Data.PERCENTAGE_MULTIPLIER

        monthly_stats = monthly_stats.fillna(Data.DEFAULT_FILL_VALUE)
        monthly_stats[Columns.MONTH] = monthly_stats[Columns.MONTH].astype(str)

        # Melt the DataFrame to long format for Plotly Express
        monthly_stats_melted = monthly_stats.melt(id_vars=[Columns.MONTH, Columns.TOTAL_SHOTS_TREND], 
                                                  value_vars=[Columns.GOAL_PERCENTAGE_TREND, Columns.SAVED_PERCENTAGE_TREND, Columns.OUT_PERCENTAGE_TREND],
                                                  var_name=Columns.OUTCOME_TYPE, value_name=Columns.PERCENTAGE)

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
        df[Columns.DATE] = pd.to_datetime(df[Columns.DATE])

        if start_date and end_date:
            df = df[(df[Columns.DATE] >= pd.Timestamp(start_date)) & (df[Columns.DATE] <= pd.Timestamp(end_date))]

        df[Columns.MONTH] = df[Columns.DATE].dt.to_period('M').astype(str)

        monthly_outcome_counts = df.groupby([Columns.MONTH, Columns.STATUS]).size().unstack(fill_value=Data.DEFAULT_FILL_VALUE)
        monthly_outcome_percentages = monthly_outcome_counts.apply(lambda x: x / x.sum() * Data.PERCENTAGE_MULTIPLIER, axis=1)
        monthly_outcome_percentages = monthly_outcome_percentages.reset_index()

        # Melt the DataFrame to long format for Plotly Express
        monthly_outcome_percentages_melted = monthly_outcome_percentages.melt(id_vars=[Columns.MONTH], var_name=Columns.STATUS, value_name=Columns.GOAL_PERCENTAGE)

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
        keeper_data = data[data[Columns.KEEPER_NAME] == keeper_name].copy()
        keeper_data[Columns.DATE] = pd.to_datetime(keeper_data[Columns.DATE])

        if start_date and end_date:
            keeper_data = keeper_data[(keeper_data[Columns.DATE] >= pd.Timestamp(start_date)) & (keeper_data[Columns.DATE] <= pd.Timestamp(end_date))]
        
        # Count goals conceded (status == 'goal'), saves (status == 'saved'), and outs (status == 'out')
        goals_conceded = len(keeper_data[keeper_data[Columns.STATUS] == Status.GOAL])
        saves = len(keeper_data[keeper_data[Columns.STATUS] == Status.SAVED])
        outs = len(keeper_data[keeper_data[Columns.STATUS] == Status.OUT])

        total_faced = goals_conceded + saves + outs

        if total_faced == Data.DEFAULT_FILL_VALUE:
            return pd.DataFrame(columns=[Columns.STATUS, Columns.COUNT])

        outcome_counts = pd.DataFrame({
            Columns.STATUS: [Status.GOAL, Status.SAVED, Status.OUT],
            Columns.COUNT: [goals_conceded, saves, outs]
        })
        
        # Calculate percentages for the pie chart
        outcome_counts[Columns.GOAL_PERCENTAGE] = (outcome_counts[Columns.COUNT] / total_faced) * Data.PERCENTAGE_MULTIPLIER

        return outcome_counts
