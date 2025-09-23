# NFT Weingarten Penalty Tracker

## Project Overview
This is a Python-based Streamlit application designed to track and visualize NFT (Non-Fungible Token) Weingarten penalty shootout data. It provides comprehensive insights into player performance, goalkeeper analysis, and overall penalty statistics through interactive dashboards and charts. The application leverages `pandas` for efficient data manipulation, `plotly-express` for creating rich and interactive visualizations, and `streamlit` for building a dynamic and user-friendly web interface.

## Key Features
The dashboard is organized into several pages, each offering a unique perspective on the penalty shootout data:
*   **Home (Overview)**: Displays overall shootout statistics, including total penalties and overall goal percentage. It also highlights top-performing players and goalkeepers based on recent data and shows the outcome distribution (goals, saves, outs).
*   **Player Performance Analysis**: Provides an in-depth look at individual player performance. It features a player leaderboard based on a custom scoring system (3 points for a goal, 0 for a save, -1 for an out) and allows for comparing multiple players' performance over customizable timeframes, showing their monthly scores, goals, saves, and out shots.
*   **Goalkeeper Performance Analysis**: Focuses on goalkeeper effectiveness, showcasing save percentages and detailed outcome distributions (goals conceded, saves, outs) for top goalkeepers over selected periods.
*   **Shot Distribution Analysis (Implied)**: The `utils.py` contains `create_shot_distribution_chart` which suggests a feature to visualize shot distribution on a goalpost grid, indicating where shots were aimed and their outcomes. This might be a planned feature or integrated into one of the existing pages.

## Data
The application primarily uses penalty shootout data from `data/penalty.csv`. If this file is not found, it gracefully falls back to `data/pseudo_penalty.csv`. The data structure includes the following key columns:
*   `Date`: The date of the shootout.
*   `Shooter Name`: The name of the player who took the shot.
*   `Keeper Name`: The name of the goalkeeper.
*   `Status`: The outcome of the shot (`'goal'`, `'saved'`, or `'out'`).
*   `Remark`: An integer code associated with the shot (e.g., `11, 12, 13, 21, 22, 23, 31, 32, 33`).
*   `Shot_X`, `Shot_Y`: (Implied from `utils.py`) Coordinates representing the shot's position on the goal.

## Building and Running
To set up the environment and run the application locally, follow these steps:

1.  **Clone the repository** (if not already cloned):
    ```bash
    git clone <your-repository-url>
    cd NFT-Weingarten-Penalty-Tracker
    ```
2.  **Create a virtual environment and install dependencies using `uv`**:
    ```bash
    uv venv
    . .venv/bin/activate
    uv pip install -r requirements.txt
    ```
3.  **Generate Pseudo Data (Optional)**: If `data/penalty.csv` is not available, you can generate synthetic data:
    ```bash
    uv run python generate_pseudo_data.py
    ```
    This will create `data/pseudo_penalty.csv`.
4.  **Run the Streamlit application**:
    ```bash
    streamlit run Home.py
    ```
    The application will then open in your default web browser.

## Development Conventions
*   **Language:** Python
*   **Framework:** Streamlit for interactive web dashboards.
*   **Data Manipulation:** `pandas` is extensively used for data loading, filtering, aggregation, and transformation.
*   **Visualization:** `plotly-express` is the primary library for generating various charts and graphs, including pie charts, bar charts, and scatter plots. `plotly.graph_objects` is used for more custom visualizations like the shot distribution chart.
*   **Constants Management:** A dedicated `Constants` class in `utils.py` centralizes all string literals, magic numbers, column names, status types, UI paths, and scoring rules, promoting code maintainability and readability.
*   **Utility Functions:** The `utils.py` file encapsulates core data processing logic, including `load_data`, `get_overall_statistics`, `calculate_player_scores`, `calculate_save_percentage`, and functions for trend analysis and shot distribution visualization.
*   **Data Loading Strategy:** The `load_data()` function in `utils.py` implements a robust data loading mechanism, prioritizing real data (`data/penalty.csv`) and falling back to pseudo-generated data (`data/pseudo_penalty.csv`) if real data is absent. It also provides user feedback through Streamlit warnings/errors.
*   **Page Structure:** The application is modularized into distinct Streamlit pages (`Home.py`, `pages/1_Player_Performance.py`, `pages/2_Goalkeeper_Analysis.py`), each focusing on a specific aspect of the analysis.
*   **Caching:** Streamlit's `@st.cache_data` decorator is used on data-intensive functions (e.g., `get_overall_statistics`, `calculate_player_scores`) to optimize performance by caching function outputs.
*   **UI/UX:** The application uses a dark theme (`.streamlit/config.toml`) and incorporates various UI elements like columns, metrics, date inputs, multiselects, and tabs for an enhanced user experience. Emojis are used for page icons and informational messages.