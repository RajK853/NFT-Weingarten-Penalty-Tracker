import streamlit as st
import pandas as pd
import plotly.express as px
from itertools import product

class Constants:
    # Column Names
    DATE_COL = "Date"
    SHOOTER_NAME_COL = "Shooter Name"
    KEEPER_NAME_COL = "Keeper Name"
    STATUS_COL = "Status"
    SHOOT_POSITION_COL = "Shoot Position"
    GOALS_COL = "Goals"
    MISSES_COL = "Misses"
    TOTAL_SHOTS_COL = "Total Shots"
    GOAL_PERCENTAGE_COL = "Goal Percentage"
    COUNT_COL = "Count"
    SAVE_PERCENTAGE_COL = "Save Percentage"
    TOTAL_SAVES_COL = "Total Saves"
    TOTAL_FACED_COL = "Total Faced"

    # Statuses
    GOAL_STATUS = "goal"
    SAVED_STATUS = "saved"
    OUT_STATUS = "out"

    # UI
    LOGO_PATH = "data/logo.jpg"
    LOGO_WIDTH = 100
    
    MAX_PLAYER_SELECTIONS = 5
    SCATTER_POINT_SIZE = 8

def load_data():
    data = pd.read_csv("data/penalty.csv")
    return data

def calculate_goal_percentage(data):
    goals = data[data["Status"] == "goal"].groupby("Shooter Name").size()
    misses = data[data["Status"] != "goal"].groupby("Shooter Name").size()
    
    ratio_df = pd.DataFrame({
        "Goals": goals,
        "Misses": misses
    }).fillna(0)
    
    ratio_df["Misses"] = ratio_df["Misses"].astype(int)
    ratio_df["Total Shots"] = ratio_df["Goals"] + ratio_df["Misses"]
    ratio_df[Constants.GOAL_PERCENTAGE_COL] = (ratio_df["Goals"] / ratio_df["Total Shots"]) * 100
    ratio_df[Constants.GOAL_PERCENTAGE_COL] = ratio_df[Constants.GOAL_PERCENTAGE_COL].fillna(0) # Handle division by zero
    
    return ratio_df.sort_values(by=Constants.GOAL_PERCENTAGE_COL, ascending=False)

def get_shoot_position_goals(data, player_name):
    player_goals = data[(data["Shooter Name"] == player_name) & (data["Status"] == "goal")]
    shoot_position_counts = player_goals["Shoot Position"].value_counts().reset_index()
    shoot_position_counts.columns = [Constants.SHOOT_POSITION_COL, Constants.COUNT_COL]
    return shoot_position_counts

def get_player_status_counts_over_time(data, selected_players):
    if not selected_players:
        return pd.DataFrame() # Return empty DataFrame if no players selected

    filtered_data = data[data["Shooter Name"].isin(selected_players)].copy()
    filtered_data["Date"] = pd.to_datetime(filtered_data["Date"])

    # Count occurrences of each status for each player per day
    status_counts = filtered_data.groupby(["Date", "Shooter Name", "Status"]).size().reset_index(name="Count")

    # Ensure all statuses are present for each date and player for consistent plotting
    all_dates = filtered_data["Date"].unique()
    all_statuses = filtered_data["Status"].unique()
    
    # Create a complete grid of all combinations
    idx = pd.MultiIndex.from_product([all_dates, selected_players, all_statuses], names=["Date", "Shooter Name", "Status"])
    full_df = pd.DataFrame(index=idx).reset_index()

    # Merge with actual counts, filling missing with 0
    status_counts_full = pd.merge(full_df, status_counts, on=["Date", "Shooter Name", "Status"], how="left").fillna(0)
    status_counts_full["Count"] = status_counts_full["Count"].astype(int)

    return status_counts_full.sort_values(by=["Date", "Shooter Name", "Status"])


def get_overall_statistics(data, num_periods=None, period_type=None):
    df = data.copy()
    if num_periods is not None and period_type is not None:
        df[Constants.DATE_COL] = pd.to_datetime(df[Constants.DATE_COL])
        latest_date = df[Constants.DATE_COL].max()
        if period_type == "Days":
            start_date = latest_date - pd.Timedelta(days=num_periods)
        elif period_type == "Months":
            start_date = latest_date - pd.DateOffset(months=num_periods)
        df = df[df[Constants.DATE_COL] >= start_date]

    total_penalties = len(df)
    goals = df[df[Constants.STATUS_COL] == Constants.GOAL_STATUS]
    overall_goal_percentage = (len(goals) / total_penalties) * 100 if total_penalties > 0 else 0

    outcome_distribution = df[Constants.STATUS_COL].value_counts(normalize=True) * 100
    outcome_distribution = outcome_distribution.reset_index()
    outcome_distribution.columns = [Constants.STATUS_COL, Constants.GOAL_PERCENTAGE_COL]

    return total_penalties, overall_goal_percentage, outcome_distribution


def calculate_save_percentage(data):
    # Penalties faced by each keeper
    penalties_faced = data.groupby(Constants.KEEPER_NAME_COL).size()

    # Saves by each keeper
    saves = data[data[Constants.STATUS_COL] == Constants.SAVED_STATUS].groupby(Constants.KEEPER_NAME_COL).size()

    # Create a DataFrame for save percentages
    keeper_stats = pd.DataFrame({
        Constants.TOTAL_FACED_COL: penalties_faced,
        Constants.TOTAL_SAVES_COL: saves
    }).fillna(0)

    keeper_stats[Constants.TOTAL_SAVES_COL] = keeper_stats[Constants.TOTAL_SAVES_COL].astype(int)
    keeper_stats[Constants.SAVE_PERCENTAGE_COL] = (keeper_stats[Constants.TOTAL_SAVES_COL] / keeper_stats[Constants.TOTAL_FACED_COL]) * 100
    keeper_stats[Constants.SAVE_PERCENTAGE_COL] = keeper_stats[Constants.SAVE_PERCENTAGE_COL].fillna(0) # Handle division by zero

    return keeper_stats.sort_values(by=Constants.SAVE_PERCENTAGE_COL, ascending=False)


def get_overall_shoot_position_success(data):
    # Total shots for each position
    total_shots_per_position = data.groupby(Constants.SHOOT_POSITION_COL).size()

    # Goals for each position
    goals_per_position = data[data[Constants.STATUS_COL] == Constants.GOAL_STATUS].groupby(Constants.SHOOT_POSITION_COL).size()

    # Create a DataFrame to calculate success rate
    position_success = pd.DataFrame({
        Constants.TOTAL_SHOTS_COL: total_shots_per_position,
        Constants.GOALS_COL: goals_per_position
    }).fillna(0)

    position_success[Constants.GOALS_COL] = position_success[Constants.GOALS_COL].astype(int)
    position_success[Constants.GOAL_PERCENTAGE_COL] = (position_success[Constants.GOALS_COL] / position_success[Constants.TOTAL_SHOTS_COL]) * 100
    position_success[Constants.GOAL_PERCENTAGE_COL] = position_success[Constants.GOAL_PERCENTAGE_COL].fillna(0)

    return position_success.sort_values(by=Constants.GOAL_PERCENTAGE_COL, ascending=False)


def get_overall_trend_data(data):
    df = data.copy()
    df[Constants.DATE_COL] = pd.to_datetime(df[Constants.DATE_COL])
    df['Month'] = df[Constants.DATE_COL].dt.to_period('M')

    monthly_stats = df.groupby('Month').apply(lambda x:
        pd.Series({
            'Total Shots': len(x),
            'Goals': len(x[x[Constants.STATUS_COL] == Constants.GOAL_STATUS])
        })
    ).reset_index()

    monthly_stats[Constants.GOAL_PERCENTAGE_COL] = (monthly_stats['Goals'] / monthly_stats['Total Shots']) * 100
    monthly_stats[Constants.GOAL_PERCENTAGE_COL] = monthly_stats[Constants.GOAL_PERCENTAGE_COL].fillna(0)
    monthly_stats['Month'] = monthly_stats['Month'].astype(str)

    return monthly_stats

def get_monthly_outcome_distribution(data):
    df = data.copy()
    df[Constants.DATE_COL] = pd.to_datetime(df[Constants.DATE_COL])
    df['Month'] = df[Constants.DATE_COL].dt.to_period('M').astype(str)

    monthly_outcome_counts = df.groupby(['Month', Constants.STATUS_COL]).size().unstack(fill_value=0)
    monthly_outcome_percentages = monthly_outcome_counts.apply(lambda x: x / x.sum() * 100, axis=1)
    monthly_outcome_percentages = monthly_outcome_percentages.reset_index()

    # Melt the DataFrame to long format for Plotly Express
    monthly_outcome_percentages_melted = monthly_outcome_percentages.melt(id_vars=['Month'], var_name=Constants.STATUS_COL, value_name=Constants.GOAL_PERCENTAGE_COL)

    return monthly_outcome_percentages_melted


