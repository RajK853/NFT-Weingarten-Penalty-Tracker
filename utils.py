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
    GOAL_RATIO_COL = "Goal-to-Miss Ratio"
    COUNT_COL = "Count"

    # Statuses
    GOAL_STATUS = "goal"
    SAVED_STATUS = "saved"
    OUT_STATUS = "out"

    # UI
    LOGO_PATH = "data/logo.jpg"
    LOGO_WIDTH = 100
    COLUMNS_RATIO = [1, 4]
    MAX_PLAYER_SELECTIONS = 5
    SCATTER_POINT_SIZE = 8

def load_data():
    data = pd.read_csv("data/penalty.csv")
    return data

def calculate_goal_miss_ratio(data):
    goals = data[data["Status"] == "goal"].groupby("Shooter Name").size()
    misses = data[data["Status"] != "goal"].groupby("Shooter Name").size()
    
    ratio_df = pd.DataFrame({
        "Goals": goals,
        "Misses": misses
    }).fillna(0)
    
    ratio_df["Misses"] = ratio_df["Misses"].astype(int)
    ratio_df["Total Shots"] = ratio_df["Goals"] + ratio_df["Misses"]
    ratio_df["Goal-to-Miss Ratio"] = (ratio_df["Goals"] / ratio_df["Total Shots"]) * 100
    ratio_df["Goal-to-Miss Ratio"] = ratio_df["Goal-to-Miss Ratio"].fillna(0) # Handle division by zero
    
    return ratio_df.sort_values(by="Goal-to-Miss Ratio", ascending=False)

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

def display_header():
    col1, col2 = st.columns(Constants.COLUMNS_RATIO)
    with col1:
        st.image(Constants.LOGO_PATH, width=Constants.LOGO_WIDTH)
    with col2:
        st.title("NFT Weingarten - Penalty Tracker")
