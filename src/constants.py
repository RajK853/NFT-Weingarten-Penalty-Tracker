

class Columns:
    """
    Defines string constants for column names used throughout the application's DataFrames.
    This centralizes column naming, preventing typos and ensuring consistency.
    """

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
    """
    Defines string constants for the possible outcomes of a penalty shot.
    """

    GOAL: str = "goal"
    SAVED: str = "saved"
    OUT: str = "out"


class Scoring:
    """
    Defines constants for scoring logic and time-decay parameters.
    These values are used to calculate player and goalkeeper performance scores.
    """

    GOAL: float = +1.5  # Score awarded to a shooter for scoring a goal.
    SAVED: float = 0.0  # Score awarded to a shooter for a shot being saved.
    OUT: float = -1.0  # Score awarded to a shooter for a shot going out.
    KEEPER_GOAL: float = -1.0  # Score awarded to a goalkeeper for conceding a goal.
    KEEPER_SAVED: float = +1.5  # Score awarded to a goalkeeper for making a save.
    KEEPER_OUT: float = (
        0.0  # Score awarded to a goalkeeper for a shot going out (not a save, not a goal).
    )
    PERFORMANCE_HALF_LIFE_DAYS: int = (
        45  # Days until a performance is worth half its value for time-decay calculations.
    )


class Paths:
    """
    Defines file paths and URLs for data sources and assets.
    """

    LOGO: str = "data/logo.jpg"
    DATA_PSEUDO: str = "data/pseudo_penalty.csv"
    GOOGLE_SHEET_URL_MALE: str = (
        "https://docs.google.com/spreadsheets/d/1ehIA2Ea_8wCMy5ICmwFl14FZUPLA8ki6VQBLcGqsVUU/gviz/tq?tqx=out:csv&sheet=RawData"
    )


class Gender:
    """
    Defines constants for gender categories.
    """

    MALE: str = "Male"
    FEMALE: str = "Female"


class SessionState:
    """
    Defines keys for Streamlit's session state to maintain application state across reruns.
    """

    GENDER: str = "gender"


class UI:
    """
    Defines constants related to the User Interface, including emojis, display limits, chart settings, and messages.
    """

    EMOJI_HOME_PAGE: str = "🏠"  # Emoji for the home page.
    MAX_PLAYER_SELECTIONS: int = (
        10  # Maximum number of players that can be selected in multi-select widgets.
    )
    MAX_NAMES_IN_METRIC_DISPLAY: int = (
        3  # Maximum number of names to display in a metric widget before truncating.
    )
    PIE_CHART_PULL_EFFECT: float = 0.05  # The 'pull' effect for slices in pie charts.
    RECENT_DAYS_FILTER: int = 365  # Default number of days for filtering recent data.
    TOP_N_PLAYERS_LEADERBOARD: int = (
        10  # Number of top players to display in leaderboards.
    )
    DEFAULT_NUM_PLAYERS_MULTISELECT: int = (
        4  # Default number of players pre-selected in multi-select.
    )
    PIE_CHART_HOLE_SIZE: float = 0.4  # Size of the hole in donut-style pie charts.
    CHART_Y_AXIS_BUFFER: float = 0.1  # Buffer for Y-axis range in charts.
    COLOR_GREEN: str = "green"  # Green color string.
    COLOR_RED: str = "red"  # Red color string.
    COLOR_LIGHTGRAY: str = "lightgray"  # Light gray color string.
    COLOR_BLUE: str = "blue"  # Blue color string.
    PLOTLY_DISPLAY_MODE_BAR: bool = False  # Whether to display Plotly's mode bar.
    PLOTLY_TEXT_POSITION_OUTSIDE: str = (
        "outside"  # Text position for Plotly annotations.
    )
    PLOTLY_SCATTER_MARKER_SIZE: int = 10  # Marker size for Plotly scatter plots.
    PLOTLY_SCATTER_MARKER_OPACITY: float = (
        0.7  # Marker opacity for Plotly scatter plots.
    )
    PLOTLY_AXIS_SHOWGRID: bool = False  # Whether to show grid lines on Plotly axes.
    PLOTLY_AXIS_ZEROLINE: bool = False  # Whether to show zero line on Plotly axes.
    PLOTLY_AXIS_VISIBLE: bool = False  # Whether Plotly axes are visible.
    PLOTLY_BG_COLOR_TRANSPARENT: str = (
        "rgba(0,0,0,0)"  # Transparent background color for Plotly.
    )
    PLOTLY_SHOW_LEGEND: bool = False  # Whether to show legend in Plotly charts.
    EMOJI_PLAYER_PAGE: str = "⚽"  # Emoji for the player performance page.
    EMOJI_GOALKEEPER_PAGE: str = "🧤"  # Emoji for the goalkeeper analysis page.
    EMOJI_INFO_SAD: str = "😔"  # Sad face emoji for info messages.
    EMOJI_INFO_CALENDAR: str = "🗓️"  # Calendar emoji for info messages.
    INFO_SELECT_DATE_RANGE: str = (
        "Please select both a start and end date for the leaderboard."  # Info message for date range selection.
    )
    INFO_NO_PLAYER_DATA: str = (
        "No data available for the selected players in {selected_month_display}. Please select different players or a different month. 😔"  # Info message when no player data is found.
    )
    INFO_NO_KEEPER_DATA: str = (
        "No data available for {keeper} in {selected_month_display}. 😔"  # Info message when no keeper data is found.
    )
    INFO_SELECT_MONTH_KEEPER: str = (
        "Please select a month to view goalkeeper performance. 🗓️"  # Info message for selecting month for keeper performance.
    )
    TAB_SCORE: str = "Score"  # Tab title for score.
    TAB_GOALS: str = "Goals"  # Tab title for goals.
    TAB_SAVED: str = "Saved"  # Tab title for saved shots.
    TAB_OUT: str = "Out"  # Tab title for shots out.
    TOP_N_KEEPERS_DISPLAY: int = 5  # Number of top keepers to display.
    GOAL_POST_WIDTH_VISUAL: int = 600  # Visual width of the goal post.
    GOAL_POST_HEIGHT_VISUAL: int = 400  # Visual height of the goal post.
    DEFAULT_PLOT_WIDTH: int = 600  # Default width for plots to maintain 3:2 aspect ratio.
    DEFAULT_PLOT_HEIGHT: int = 400  # Default height for plots to maintain 3:2 aspect ratio.


class Data:
    """
    Defines constants related to data processing, default values, and animation timings.
    """

    PERCENTAGE_MULTIPLIER: int = (
        100  # Multiplier to convert a fraction to a percentage.
    )
    DEFAULT_FILL_VALUE: int = 0  # Default value used for filling missing data.
    DATE_OFFSET_MONTHS_ONE: int = 1  # Offset for one month in date calculations.
    DATE_OFFSET_DAYS_ONE: int = 1  # Offset for one day in date calculations.
    DATE_DAY_ONE: int = 1  # Represents the first day of a month.
    TYPING_ANIMATION_TIMEOUT: float = 0.2  # Timeout for typing animation effects.
    MIN_DAYS_PER_WEEK: int = 3  # Minimum number of days considered for a week.
    MAX_DAYS_PER_WEEK: int = 4  # Maximum number of days considered for a week.
    SCORE_DECIMAL_PLACES: int = 2  # Number of decimal places for displaying scores.


class GoalVisual:
    """
    Defines constants for the visual representation of the goal and penalty area.
    These are used for rendering the shot map and goal visualization.
    """

    GOAL_WIDTH: int = 400  # Width of the goal in pixels for visualization.
    GOAL_HEIGHT: int = 300  # Height of the goal in pixels for visualization.
    GOAL_POST_LINE_WIDTH: int = 10  # Line width for goal posts.
    GOAL_POST_COLOR: str = "white"  # Color of the goal posts.
    PITCH_COLOR: str = "lightgreen"  # Color of the penalty pitch area.
