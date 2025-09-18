# Penalty Shootout Dashboard

This project creates an interactive web-based dashboard using Streamlit to visualize penalty shootout data. The dashboard provides key statistics, player performance over time, and goal distribution by shoot position.

## Features

-   **Top 10 Players**: Displays the top 10 players based on their goal-to-miss ratio.
-   **Player Performance Over Time**: Visualizes a selected player's goal-to-miss ratio trend over different dates.
-   **Goal Distribution by Shoot Position**: Shows a bar chart of a selected player's goals across various shoot positions.

## Data

The dashboard uses penalty shootout data from `data/penalty.csv`. The CSV file contains the following columns:

-   `Date`: The date of the shootout.
-   `Shooter Name`: The name of the player who took the shot.
-   `Keeper Name`: The name of the goalkeeper.
-   `Status`: The outcome of the shot ('goal', 'saved', or 'out').
-   `Shoot Position`: The location where the shot was aimed (e.g., 'top-left', 'center-right').

## Local Setup

To run this project locally, follow these steps:

1.  **Clone the repository**:
    ```bash
    git clone <your-repository-url>
    cd penalty-shootout-dashboard
    ```

2.  **Create a virtual environment and install dependencies using `uv`**:
    ```bash
    uv venv
    . .venv/bin/activate
    uv pip install -r requirements.txt
    ```

3.  **Run the Streamlit application**:
    ```bash
    uv run streamlit run app.py
    ```

    The application will open in your web browser.

## Deployment

This application is designed to be deployed on Streamlit Cloud. Ensure your project is pushed to a GitHub repository, and then connect it to Streamlit Cloud for deployment.
