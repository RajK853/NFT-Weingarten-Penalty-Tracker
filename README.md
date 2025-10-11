# NFT Weingarten Penalty Tracker

This is a Python-based Streamlit application designed to track and visualize NFT (Non-Fungible Token) Weingarten penalty shootout data. It provides comprehensive insights into player performance, goalkeeper analysis, and overall penalty statistics through interactive dashboards and charts.

## Key Features

The dashboard is organized into several pages, each offering a unique perspective on the penalty shootout data:
*   **Home (Overview)**: Displays overall shootout statistics, including total penalties and overall goal percentage. It also highlights top-performing players and goalkeepers based on recent data and shows the outcome distribution (goals, saves, outs).
*   **Player Performance Analysis**: Provides an in-depth look at individual player performance. It features a player leaderboard based on a custom scoring system (3 points for a goal, 0 for a save, -1 for an out) and allows for comparing multiple players' performance over customizable timeframes, showing their monthly scores, goals, saves, and out shots.
*   **Goalkeeper Performance Analysis**: Focuses on goalkeeper effectiveness, showcasing a time-weighted score based on the outcome of shots faced (goal: -1.0, saved: +1.5, out: 0.0) and detailed outcome distributions for top goalkeepers over selected periods.

## Data

The application primarily uses penalty shootout data from `data/penalty.csv`. If this file is not found, it gracefully falls back to `data/pseudo_penalty.csv`. The data structure includes the following key columns:
*   `Date`: The date of the shootout.
*   `Shooter Name`: The name of the player who took the shot.
*   `Keeper Name`: The name of the goalkeeper.
*   `Status`: The outcome of the shot (`'goal'`, `'saved'`, or `'out'`).

## Building and Running

To set up the environment and run the application locally, follow these steps:

1.  **Clone the repository**:
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

## Deployment

This application is designed to be deployed on Streamlit Cloud. Ensure your project is pushed to a GitHub repository, and then connect it to Streamlit Cloud for deployment.