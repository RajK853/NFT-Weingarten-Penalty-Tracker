from datetime import date
from typing import List, Tuple

import pandas as pd
import streamlit as st

from src.constants import Columns, Status

@st.cache_data
def get_recent_penalties(data: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """
    Retrieves the most recent penalty shootout records from the dataset.

    This function is useful for quickly viewing the latest activity in the penalty shootout data.

    Args:
        data (pd.DataFrame): The input DataFrame containing penalty shootout data.
        n (int): The number of most recent penalties to retrieve. Defaults to 5.

    Returns:
        pd.DataFrame: A DataFrame containing the last `n` penalty records.
                      If the DataFrame has fewer than `n` records, all records are returned.
    """
    return data.tail(n)

@st.cache_data
def get_longest_goal_streak(data: pd.DataFrame) -> Tuple[List[str], int]:
    """
    Calculates the longest goal streak achieved by any player and identifies all players who achieved it.

    A goal streak is defined as consecutive goals scored by a single player. This function iterates
    through each player's penalty records to find their individual longest streak and then determines
    the maximum streak across all players.

    Args:
        data (pd.DataFrame): The input DataFrame containing penalty shootout data, including
                             `Columns.SHOOTER_NAME` and `Columns.STATUS`.

    Returns:
        Tuple[List[str], int]: A tuple containing:
            - streaking_players (List[str]): A list of names of players who achieved the longest goal streak.
            - longest_streak (int): The length of the longest goal streak found.
                                    Returns ([], 0) if the input DataFrame is empty or lacks necessary columns.
    """
    longest_streak = 0
    streaking_players = []

    if data.empty or Columns.SHOOTER_NAME not in data.columns:
        return [], 0

    for player in data[Columns.SHOOTER_NAME].unique():
        player_data = data[data[Columns.SHOOTER_NAME] == player]
        current_streak = 0
        max_player_streak = 0
        
        for status in player_data[Columns.STATUS]:
            if status == Status.GOAL:
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
    """
    Identifies the player who scored the most goals in a single session (on a specific date).

    This function groups the goal-scoring records by date and shooter to find the maximum number
    of goals scored by any single player within one day.

    Args:
        data (pd.DataFrame): The input DataFrame containing penalty shootout data, including
                             `Columns.DATE`, `Columns.SHOOTER_NAME`, and `Columns.STATUS`.

    Returns:
        Tuple[str, date, int]: A tuple containing:
            - shooter_name (str): The name of the player who scored the most goals.
            - session_date (date): The date of the session when the goals were scored.
            - goal_count (int): The number of goals scored in that session.
                                Returns (None, None, 0) if no goals are found in the data.
    """
    goals_in_session = data[data[Columns.STATUS] == Status.GOAL].groupby([Columns.DATE, Columns.SHOOTER_NAME]).size().reset_index(name='goals')
    if not goals_in_session.empty:
        most_goals = goals_in_session.loc[goals_in_session['goals'].idxmax()]
        return most_goals[Columns.SHOOTER_NAME], most_goals[Columns.DATE], most_goals['goals']
    
    return None, None, 0

@st.cache_data
def get_marathon_man(data: pd.DataFrame) -> Tuple[List[str], int]:
    """
    Identifies the player(s) who have participated in the most unique penalty sessions.

    A session is defined by a unique date. This function counts the number of distinct dates
    each player has participated in and returns the player(s) with the highest count.

    Args:
        data (pd.DataFrame): The input DataFrame containing penalty shootout data, including
                             `Columns.SHOOTER_NAME` and `Columns.DATE`.

    Returns:
        Tuple[List[str], int]: A tuple containing:
            - marathon_men (List[str]): A list of names of players who participated in the most sessions.
            - max_sessions (int): The maximum number of sessions participated in.
                                  Returns ([], 0) if the input DataFrame is empty or lacks necessary columns.
    """
    if data.empty or Columns.SHOOTER_NAME not in data.columns:
        return [], 0

    session_counts = data.groupby(Columns.SHOOTER_NAME)[Columns.DATE].nunique()
    
    if session_counts.empty:
        return [], 0
        
    max_sessions = session_counts.max()
    
    if max_sessions == 0:
        return [], 0
        
    marathon_men = session_counts[session_counts == max_sessions].index.tolist()
    
    return marathon_men, int(max_sessions)

@st.cache_data
def get_mysterious_ninja(data: pd.DataFrame) -> Tuple[List[str], int]:
    """
    Identifies the player(s) who have participated in the fewest unique penalty sessions.

    A session is defined by a unique date. This function counts the number of distinct dates
    each player has participated in and returns the player(s) with the lowest count.

    Args:
        data (pd.DataFrame): The input DataFrame containing penalty shootout data, including
                             `Columns.SHOOTER_NAME` and `Columns.DATE`.

    Returns:
        Tuple[List[str], int]: A tuple containing:
            - mysterious_ninjas (List[str]): A list of names of players who participated in the fewest sessions.
            - min_sessions (int): The minimum number of sessions participated in.
                                  Returns ([], 0) if the input DataFrame is empty or lacks necessary columns.
    """
    if data.empty or Columns.SHOOTER_NAME not in data.columns:
        return [], 0

    session_counts = data.groupby(Columns.SHOOTER_NAME)[Columns.DATE].nunique()
    
    if session_counts.empty:
        return [], 0
        
    min_sessions = session_counts.min()
    
    if min_sessions == 0:
        return [], 0
        
    mysterious_ninjas = session_counts[session_counts == min_sessions].index.tolist()
    
    return mysterious_ninjas, int(min_sessions)

@st.cache_data
def get_busiest_day(data: pd.DataFrame) -> Tuple[date, int]:
    """
    Identifies the date on which the most penalties were taken.

    This function groups the penalty shootout data by date and counts the total number of penalties
    recorded for each day, then returns the date with the highest count.

    Args:
        data (pd.DataFrame): The input DataFrame containing penalty shootout data, including `Columns.DATE`.

    Returns:
        Tuple[date, int]: A tuple containing:
            - busiest_day (date): The date with the highest number of penalties.
            - penalty_count (int): The total number of penalties taken on that day.
                                   Returns (None, 0) if the input DataFrame is empty.
    """
    day_counts = data.groupby(Columns.DATE).size()
    if not day_counts.empty:
        busiest_day = day_counts.idxmax()
        return busiest_day, day_counts.max()
    return None, 0

@st.cache_data
def get_biggest_rivalry(data: pd.DataFrame) -> Tuple[str, str, int]:
    """
    Identifies the most frequent shooter-keeper matchup (rivalry).

    This function counts the occurrences of each unique combination of shooter and goalkeeper
    and returns the pair that has faced each other the most times.

    Args:
        data (pd.DataFrame): The input DataFrame containing penalty shootout data, including
                             `Columns.SHOOTER_NAME` and `Columns.KEEPER_NAME`.

    Returns:
        Tuple[str, str, int]: A tuple containing:
            - shooter_name (str): The name of the shooter in the most frequent rivalry.
            - keeper_name (str): The name of the goalkeeper in the most frequent rivalry.
            - encounters (int): The number of times this shooter-keeper pair has faced each other.
                                Returns (None, None, 0) if the input DataFrame is empty or lacks necessary columns.
    """
    rivalry_counts = data.groupby([Columns.SHOOTER_NAME, Columns.KEEPER_NAME]).size().reset_index(name='encounters')
    if not rivalry_counts.empty:
        biggest_rivalry = rivalry_counts.loc[rivalry_counts['encounters'].idxmax()]
        return biggest_rivalry[Columns.SHOOTER_NAME], biggest_rivalry[Columns.KEEPER_NAME], biggest_rivalry['encounters']
    
    return None, None, 0

@st.cache_data
def get_most_saves_in_session(data: pd.DataFrame) -> Tuple[str, date, int]:
    """
    Identifies the goalkeeper who made the most saves in a single session (on a specific date).

    This function groups the save records by date and goalkeeper to find the maximum number
    of saves made by any single goalkeeper within one day.

    Args:
        data (pd.DataFrame): The input DataFrame containing penalty shootout data, including
                             `Columns.DATE`, `Columns.KEEPER_NAME`, and `Columns.STATUS`.

    Returns:
        Tuple[str, date, int]: A tuple containing:
            - keeper_name (str): The name of the goalkeeper who made the most saves.
            - session_date (date): The date of the session when the saves were made.
            - save_count (int): The number of saves made in that session.
                                Returns (None, None, 0) if no saves are found in the data.
    """
    saves_in_session = data[data[Columns.STATUS] == Status.SAVED].groupby([Columns.DATE, Columns.KEEPER_NAME]).size().reset_index(name='saves')
    if not saves_in_session.empty:
        most_saves = saves_in_session.loc[saves_in_session['saves'].idxmax()]
        return most_saves[Columns.KEEPER_NAME], most_saves[Columns.DATE], most_saves['saves']
    
    return None, None, 0
