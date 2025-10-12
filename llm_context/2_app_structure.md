# Application Structure

The application is a multi-page Streamlit dashboard.

*   `Home.py`: Main entry point, showing an overview.
*   `pages/`: Contains the other pages of the application.
    *   `1_Player_Performance.py`: Player performance analysis.
    *   `2_Goalkeeper_Analysis.py`: Goalkeeper performance analysis.
*   `src/`: Contains the core logic.
    *   `analysis.py`: Functions for statistics and scores.
    *   `constants.py`: Application constants.
    *   `data_loader.py`: Data loading logic.
    *   `plotting.py`: Visualization functions.
    *   `records.py`: Record calculation functions.
    *   `ui.py`: UI helper functions.
