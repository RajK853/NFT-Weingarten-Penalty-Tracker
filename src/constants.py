from typing import List
import numpy as np

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
    KEEPER_GOAL: float = -1.0
    KEEPER_SAVED: float = +1.5
    KEEPER_OUT: float = 0.0
    PERFORMANCE_HALF_LIFE_DAYS: int = 45 # Days until a performance is worth half its value.


class Paths:
    LOGO: str = "data/logo.jpg"
    DATA_PSEUDO: str = "data/pseudo_penalty.csv"
    GOOGLE_SHEET_URL_MALE: str = "https://docs.google.com/spreadsheets/d/1ehIA2Ea_8wCMy5ICmwFl14FZUPLA8ki6VQBLcGqsVUU/gviz/tq?tqx=out:csv&sheet=RawData"
    
class Gender:
    MALE: str = "Male"
    FEMALE: str = "Female"

class SessionState:
    GENDER: str = "gender"

class UI:
    EMOJI_HOME_PAGE: str = "🏠"
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
    PLOTLY_TEXT_POSITION_OUTSIDE: str = 'outside'
    PLOTLY_SCATTER_MARKER_SIZE: int = 10
    PLOTLY_SCATTER_MARKER_OPACITY: float = 0.7
    PLOTLY_AXIS_SHOWGRID: bool = False
    PLOTLY_AXIS_ZEROLINE: bool = False
    PLOTLY_AXIS_VISIBLE: bool = False
    PLOTLY_BG_COLOR_TRANSPARENT: str = 'rgba(0,0,0,0)'
    PLOTLY_SHOW_LEGEND: bool = False
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
    SCORE_DECIMAL_PLACES: int = 2

class GoalVisual:
    GOAL_WIDTH: int = 400
    GOAL_HEIGHT: int = 300
    GOAL_POST_LINE_WIDTH: int = 10
    GOAL_POST_COLOR: str = "white"
    PITCH_COLOR: str = "lightgreen"
    GRID_DIMENSION: int = 3 # For 3x3 grid
    GRID_LINES: int = 10
    GRID_SQUARE_SIZE: int = 20