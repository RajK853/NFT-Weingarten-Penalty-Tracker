## Refactoring Plan: Clarity, Maintainability, and Simplicity

**Overall Strategy:**

1.  **Identify Boilerplate/Redundancy:** Look for repetitive code, magic numbers/strings not yet in constants, and overly complex logic.
2.  **Improve Readability:** Focus on clear variable names, consistent formatting, and breaking down large functions.
3.  **Apply Best Practices:** Consider Pythonic idioms, Streamlit best practices (e.g., session state management, caching), and general software engineering principles (e.g., DRY - Don't Repeat Yourself).
4.  **Modularity:** Ensure functions and modules have clear responsibilities.

**Detailed Plan (Atomic Steps):**

---

### Phase 1: Constants and Imports Cleanup

- [x] **Step 1.1: Review `src/constants.py`**
    - **Task:** Ensure all relevant magic numbers/strings are constants. Check for any unused constants.
    - **Rationale:** Centralizes configuration, improves readability, and reduces errors.

- [x] **Step 1.2: Review Imports**
    - **Task:** Go through all Python files (`Home.py`, `pages/*.py`, `src/*.py`) and ensure imports are minimal, necessary, and ordered consistently (e.g., standard library, third-party, local modules). Remove unused imports.
    - **Rationale:** Reduces clutter, improves load times, and clarifies dependencies.

### Phase 2: UI/Streamlit Refactoring

- [x] **Step 2.1: Centralize Common UI Elements**
    - **Task:** Create a function in `src/ui.py` for the common header (logo, title, description) used across `Home.py` and `pages/*.py`.
    - **Rationale:** Reduces boilerplate, ensures consistency, and simplifies future UI changes.

- [x] **Step 2.2: Streamlit Session State Management**
    - **Task:** Review `Home.py` and other pages for `st.session_state` initialization. Ensure it's done cleanly and consistently.
    - **Rationale:** Improves clarity and prevents potential issues with state management.

### Phase 3: Data Loading and Preprocessing

- [x] **Step 3.1: Review `src/data_loader.py`**
    - **Task:** Ensure `load_data` is efficient and handles edge cases gracefully. Check for any redundant data preprocessing steps.
    - **Rationale:** Optimizes performance and ensures data integrity.

### Phase 4: Analysis Logic Refactoring (`src/analysis.py`)

- [x] **Step 4.1: Simplify `_get_date_range_from_month_display`**
    - **Task:** Make this helper function more concise if possible.
    - **Rationale:** Improves readability.

- [x] **Step 4.2: Consolidate Time-Decay Logic**
    - **Task:** Create a helper function (e.g., `_apply_time_decay`) that encapsulates the `days_ago`, `weight`, and `decay_rate` calculation. This function would take a DataFrame and return it with `days_ago` and `weight` columns.
    - **Rationale:** Avoids repetition in `calculate_player_scores` and `calculate_time_weighted_save_percentage`.

- [x] **Step 4.3: Refactor `calculate_player_scores`**
    - **Task:** Use the new `_apply_time_decay` helper. Streamline score aggregation.
    - **Rationale:** Improves clarity and maintainability.

- [x] **Step 4.4: Refactor `calculate_time_weighted_save_percentage`**
    - **Task:** Use the new `_apply_time_decay` helper. Streamline aggregation.
    - **Rationale:** Improves clarity and maintainability.

- [x] **Step 4.5: Review other `src/analysis.py` functions**
    - **Task:** Check `get_overall_statistics`, `get_player_status_counts_over_time`, `calculate_save_percentage`, `get_overall_trend_data`, `get_monthly_outcome_distribution`, `get_keeper_outcome_distribution` for clarity and potential improvements.
    - **Rationale:** Ensures consistency and efficiency across all analysis functions.

### Phase 5: Page-Specific Refactoring

- [x] **Step 5.1: Refactor `pages/1_Player_Performance.py`**
    - **Task:** Apply common UI elements. Review chart generation for clarity.
    - **Rationale:** Improves readability and consistency.

- [x] **Step 5.2: Refactor `pages/2_Goalkeeper_Analysis.py`**
    - **Task:** Apply common UI elements. Review chart generation for clarity.
    - **Rationale:** Improves readability and consistency.

- [x] **Step 5.3: Refactor `Home.py`**
    - **Task:** Apply common UI elements. Review record display logic for clarity.
    - **Rationale:** Improves readability and consistency.

### Phase 6: Final Review and Cleanup

- [x] **Step 6.1: Code Style and Comments**
    - **Task:** Ensure consistent code style (PEP 8 where applicable). Review comments for clarity and necessity.
    - **Rationale:** Improves long-term maintainability.

- [x] **Step 6.2: Type Hinting**
    - **Task:** Ensure type hints are consistently applied and accurate.
    - **Rationale:** Improves code understanding and enables static analysis.