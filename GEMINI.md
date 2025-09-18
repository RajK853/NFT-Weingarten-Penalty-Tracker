# Project Context: Penalty Shootout Dashboard

## Objective
The primary goal of this project is to create an interactive web-based dashboard that visualizes penalty shootout data from a CSV file. The dashboard should be accessible online and provide key statistics to users.

## Scope
The project involves:
1.  Reading and processing a CSV file with penalty shootout data.
2.  Using Python to analyze the data and generate key statistics.
3.  Building an interactive web page using the Streamlit framework.
4.  Deploying the Streamlit application for online access.

## Data Schema
The input data is a CSV file (`data/penalty.csv`) with the following columns:
-   **Date**: The date of the shootout.
-   **Shooter Name**: The name of the player who took the shot.
-   **Keeper Name**: The name of the goalkeeper.
-   **Status**: The outcome of the shot, which can be 'goal', 'saved', or 'out'.
-   **Shoot Position**: The location where the shot was aimed, such as 'top-left', 'center-right', etc.

## Technology Stack
-   **Language**: Python 3.10+
-   **Package Manager**: `uv` (preferred for speed and efficiency).
-   **Core Libraries**: `pandas` for data manipulation, `streamlit` for the web application, and `plotly.express` for interactive charts.
-   **Deployment**: Streamlit Cloud, requiring a GitHub repository.

## Instructions for Gemini CLI
-   **Code Style**: Adhere to PEP 8 standards. Use clear variable names and add comments for complex logic.
-   **Environment Setup**: Always use `uv` for managing dependencies. The first step should be to create a virtual environment with `uv venv` and install the required packages using `uv pip install -r requirements.txt`.
-   **Error Handling**: Implement robust error handling, especially for file I/O operations (e.g., if the CSV file is not found).
-   **Modularity**: Break down the code into logical functions and classes where appropriate to improve readability and maintainability.
-   **User Interface**: Use `streamlit` components to create a clean, intuitive, and interactive user interface. Ensure the dashboard is responsive and works well on different screen sizes.
-   **String Literals**: Always use double quotation marks (`"`) for string literals.
