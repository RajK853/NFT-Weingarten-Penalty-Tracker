# Project Tasks: Penalty Shootout Dashboard

## Phase 1: Project Setup and Data Ingestion
-   [ ] **Task 1.1**: Create a new directory for the project.
-   [ ] **Task 1.2**: Initialize a Git repository and commit the initial project structure.
-   [ ] **Task 1.3**: Create a `requirements.txt` file listing `pandas`, `streamlit`, and `plotly-express`.
-   [ ] **Task 1.4**: Use `uv` to create a virtual environment and install the dependencies from `requirements.txt`.
-   [ ] **Task 1.5**: Write a Python script (`app.py`) to read the CSV data into a pandas DataFrame. Include a basic `st.dataframe()` to display the raw data for verification.

## Phase 2: Data Analysis and Statistics Calculation
-   [ ] **Task 2.1**: Add a function to calculate the goal-to-miss ratio for each player. A "miss" is defined as a 'saved' or 'out' status.
-   [ ] **Task 2.2**: Sort the players by their goal-to-miss ratio and identify the top 10.
-   [ ] **Task 2.3**: Create a function to group the data by `Shooter Name` and `Date` to track a player's performance over time.
-   [ ] **Task 2.4**: Create a function to count the number of goals for each `Shoot Position` for each player.

## Phase 3: Interactive Dashboard Development
-   [ ] **Task 3.1**: Design the main layout of the Streamlit app.
-   [ ] **Task 3.2**: Implement a sidebar with a dropdown menu to select a `Shooter Name`.
-   [ ] **Task 3.3**: Display the list of top 10 players with their goal-to-miss ratio in a clear format (e.g., `st.table` or `st.dataframe`).
-   [ ] **Task 3.4**: Based on the selected player, display their performance over time using an interactive line chart created with `plotly.express`.
-   [ ] **Task 3.5**: For the selected player, visualize their goal positions using a bar chart showing the count of goals for each `Shoot Position`.

## Phase 4: Deployment
-   [ ] **Task 4.1**: Create a `README.md` file explaining the project, how to run it locally, and what the dashboard shows.
-   [ ] **Task 4.2**: Push the entire project to a new GitHub repository.
-   [ ] **Task 4.3**: Deploy the app using Streamlit Cloud by connecting it to the GitHub repository.
