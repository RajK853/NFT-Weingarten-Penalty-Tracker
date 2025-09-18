# Project Tasks: Penalty Shootout Dashboard

## Phase 1: Project Setup and Data Ingestion
-   [x] **Task 1.1**: Create a new directory for the project.
-   [x] **Task 1.2**: Initialize a Git repository and commit the initial project structure.
-   [x] **Task 1.3**: Create a `requirements.txt` file listing `pandas`, `streamlit`, and `plotly-express`.
-   [x] **Task 1.4**: Use `uv` to create a virtual environment and install the dependencies from `requirements.txt`.
-   [x] **Task 1.5**: Write a Python script (`app.py`) to read the CSV data into a pandas DataFrame. Include a basic `st.dataframe()` to display the raw data for verification.

## Phase 2: Data Analysis and Statistics Calculation
-   [x] **Task 2.1**: Add a function to calculate the goal-to-miss ratio for each player. A "miss" is defined as a 'saved' or 'out' status.
-   [x] **Task 2.2**: Sort the players by their goal-to-miss ratio and identify the top 10.
-   [x] **Task 2.3**: Create a function to group the data by `Shooter Name` and `Date` to track a player's performance over time.
-   [x] **Task 2.4**: Create a function to count the number of goals for each `Shoot Position` for each player.

## Phase 3: Interactive Dashboard Development
-   [x] **Task 3.1**: Design the main layout of the Streamlit app.
-   [x] **Task 3.2**: Implement a sidebar with a dropdown menu to select a `Shooter Name`.
-   [x] **Task 3.3**: Display the list of top 10 players with their goal-to-miss ratio in a clear format (e.g., `st.table` or `st.dataframe`).
-   [x] **Task 3.4**: Based on the selected player, display their performance over time using an interactive line chart created with `plotly.express`.
-   [x] **Task 3.5**: For the selected player, visualize their goal positions using a bar chart showing the count of goals for each `Shoot Position`.
-   [x] **Task 3.6**: Reorganize plots into separate Streamlit pages based on their categories (Overview, Player Performance, Goalkeeper Analysis, Shot Distribution).
-   [x] **Task 3.7**: Add a filter to select the number of recent months for the "Overall Shoot Position Effectiveness" plot.
-   [x] **Task 3.8**: Implement caching (`st.cache_data`) for data loading and computationally intensive functions to improve performance.

## Phase 4: Deployment
-   [x] **Task 4.1**: Create a `README.md` file explaining the project, how to run it locally, and what the dashboard shows.
-   [ ] **Task 4.2**: Push the entire project to a new GitHub repository.
-   [ ] **Task 4.3**: Deploy the app using Streamlit Cloud by connecting it to the GitHub repository.