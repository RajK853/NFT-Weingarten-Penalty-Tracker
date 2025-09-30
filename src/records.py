from datetime import date
from typing import List, Tuple
import pandas as pd
import streamlit as st
from src.constants import Columns, Status

@st.cache_data
def get_recent_penalties(data: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Returns the last n penalties."""
    return data.tail(n)

@st.cache_data
def get_longest_goal_streak(data: pd.DataFrame) -> Tuple[List[str], int]:
    """Calculates the longest goal streak and returns all players who achieved it."""
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
    """Finds the player who scored the most goals in a single session."""
    goals_in_session = data[data[Columns.STATUS] == Status.GOAL].groupby([Columns.DATE, Columns.SHOOTER_NAME]).size().reset_index(name='goals')
    if not goals_in_session.empty:
        most_goals = goals_in_session.loc[goals_in_session['goals'].idxmax()]
        return most_goals[Columns.SHOOTER_NAME], most_goals[Columns.DATE], most_goals['goals']
    
    return None, None, 0

@st.cache_data
def get_marathon_man(data: pd.DataFrame) -> Tuple[List[str], int]:
    """Finds the player(s) who have participated in the most sessions."""
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
    """Finds the player(s) who have participated in the fewest sessions."""
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
    """Finds the date with the most penalties taken."""
    day_counts = data.groupby(Columns.DATE).size()
    if not day_counts.empty:
        busiest_day = day_counts.idxmax()
        return busiest_day, day_counts.max()
    return None, 0

@st.cache_data
def get_biggest_rivalry(data: pd.DataFrame) -> Tuple[str, str, int]:
    """Finds the most frequent shooter-keeper matchup."""
    rivalry_counts = data.groupby([Columns.SHOOTER_NAME, Columns.KEEPER_NAME]).size().reset_index(name='encounters')
    if not rivalry_counts.empty:
        biggest_rivalry = rivalry_counts.loc[rivalry_counts['encounters'].idxmax()]
        return biggest_rivalry[Columns.SHOOTER_NAME], biggest_rivalry[Columns.KEEPER_NAME], biggest_rivalry['encounters']
    
    return None, None, 0

@st.cache_data
def get_most_saves_in_session(data: pd.DataFrame) -> Tuple[str, date, int]:
    """Finds the keeper who saved the most goals in a single session."""
    saves_in_session = data[data[Columns.STATUS] == Status.SAVED].groupby([Columns.DATE, Columns.KEEPER_NAME]).size().reset_index(name='saves')
    if not saves_in_session.empty:
        most_saves = saves_in_session.loc[saves_in_session['saves'].idxmax()]
        return most_saves[Columns.KEEPER_NAME], most_saves[Columns.DATE], most_saves['saves']
    
    return None, None, 0
