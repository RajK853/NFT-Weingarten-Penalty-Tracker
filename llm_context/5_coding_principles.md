# Coding Principles and Best Practices

This document outlines the key principles and strategies for developing this project. Adhering to these guidelines ensures the creation of code that is readable, maintainable, and robust.

---

## 1. Python-Specific Philosophy

These principles are central to writing effective and "Pythonic" code.

*   **The Zen of Python (PEP 20):** The guiding philosophy of Python. Key tenets include:
    *   *Readability counts.*
    *   *Simple is better than complex.*
    *   *Explicit is better than implicit.*
*   **Write "Pythonic" Code:** Utilize Python's features and idioms as they are intended.
    *   **Examples:** Use list comprehensions, context managers (`with` statements), and dictionary/set lookups for efficiency and clarity.
*   **Duck Typing:** Focus on an object's behavior, not its type. If an object has the required methods and properties, it can be used. This promotes flexibility.

---

## 2. General Software Design Principles

These are universal principles that lead to better software architecture.

*   **KISS (Keep It Simple, Stupid):** Prioritize simplicity. Avoid unnecessary complexity, as simple code is easier to understand, debug, and maintain.
*   **DRY (Don't Repeat Yourself):** Avoid code duplication. Encapsulate and reuse logic in functions, classes, or modules.
*   **YAGNI (You Ain't Gonna Need It):** Do not add functionality until it is actually needed. This keeps the codebase lean and focused.
*   **Principle of Least Astonishment (POLA):** A component of a system should behave in a way that users expect. The behavior should not be surprising or astonishing.
*   **Composition Over Inheritance:** Favor composing objects from smaller, single-responsibility components rather than creating complex inheritance hierarchies. This leads to more flexible and decoupled designs.

---

## 3. Development Strategies

These are practical strategies to apply during the development process.

*   **Modularity:** The project is structured into modules with specific responsibilities (e.g., `data_loader`, `analysis`). This separation of concerns should be maintained and extended.
*   **Readability:** Write clean, well-structured code. Use meaningful names for variables and functions, and follow consistent formatting.
*   **Error Handling & Resilience:** The application must be robust. It should anticipate potential failures (e.g., network issues, missing files) and handle them gracefully without crashing.
    *   **Fail Fast:** Report errors as soon as they are detected by raising exceptions immediately. This prevents the system from continuing in an invalid state and makes debugging easier.
*   **Documentation:**
    *   **Docstrings:** All functions, classes, and methods must have comprehensive docstrings. These should explain the purpose, arguments, and return values. Follow a consistent style (e.g., Google style).
    *   **Inline Comments:** Use inline comments sparingly for complex or non-obvious logic. Comments should explain *why* something is done, not *what* is done.
*   **Testing:**
    *   **Test-Driven Development (TDD):** While not strictly enforced, the principle of writing tests alongside implementation is encouraged to ensure correctness and prevent regressions.
    *   **Unit Tests:** Each module or function should have unit tests to verify its behavior in isolation.
*   **Security:**
    *   **Input Validation:** Never trust external data. Validate and sanitize all inputs (e.g., from data files, user-facing UI components) to prevent errors and security vulnerabilities.
    *   **No Hardcoded Secrets:** Never store sensitive information like API keys or credentials directly in the source code. Use environment variables or a secure secret management system.

---

## 4. Plotting Best Practices (Streamlit & Plotly)

To ensure a consistent and user-friendly experience across all devices, especially mobile, adhere to the following guidelines when creating plots with Plotly in Streamlit:

*   **Static Plots with Tooltips:** All plots should be static (no zooming or panning) but must retain hover tooltip information.
    *   **Disable Interactivity:** For each Plotly figure (`fig`), disable zooming and panning by adding `fig.update_layout(xaxis_fixedrange=True, yaxis_fixedrange=True)`.
    *   **Hide Mode Bar:** Always use `st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': UI.PLOTLY_DISPLAY_MODE_BAR})`. This hides the interactive mode bar (zoom, pan, etc.) while keeping tooltips active.
    *   **Import UI:** Ensure `UI` is imported from `src.constants` in any file where `UI.PLOTLY_DISPLAY_MODE_BAR` is used.
*   **Mobile-Friendly Layout:** Pay attention to legend placement and plot margins to prevent overlaps on smaller screens.
    *   **Legend Position:** For legends, consider placing them horizontally at the bottom of the plot using `fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.8, xanchor="center", x=0.5))`.
    *   **Bottom Margin:** Adjust the bottom margin to provide sufficient space for the legend and x-axis title using `fig.update_layout(margin=dict(b=200))`. These values (`y` and `b`) may need fine-tuning based on the specific plot and content.