# Penalty Shootout Dashboard

This project creates an interactive web-based dashboard using Streamlit to visualize penalty shootout data. The dashboard provides key statistics, player performance over time, and goal distribution by shoot position.

## Features

The dashboard is organized into several pages for a comprehensive analysis:

-   **Home (Overview)**: Provides overall shootout statistics, monthly outcome trends, and monthly outcome distribution.
-   **Player Performance Analysis**: Displays the top players by goal percentage and allows comparison of player performance over time.
-   **Goalkeeper Performance Analysis**: Offers insights into goalkeeper save percentages and outcome distributions.
-   **Shot Distribution Analysis**: Visualizes overall shoot position effectiveness with a monthly filter and individual player goal distribution on a goal post grid.

The application also utilizes caching to improve performance.

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
