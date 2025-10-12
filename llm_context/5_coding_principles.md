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
    *   **Fixed Range:** All plots should have `fixed_range=True` by default to prevent zooming and panning, ensuring a consistent view.
    *   **Disable Interactivity:** For each Plotly figure (`fig`), disable zooming and panning by adding `fig.update_layout(xaxis_fixedrange=True, yaxis_fixedrange=True)`.
    *   **Hide Mode Bar:** Always use `st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': UI.PLOTLY_DISPLAY_MODE_BAR})`. This hides the interactive mode bar (zoom, pan, etc.) while keeping tooltips active.
    *   **Import UI:** Ensure `UI` is imported from `src.constants` in any file where `UI.PLOTLY_DISPLAY_MODE_BAR` is used.
*   **Mobile-Friendly Layout:** Pay attention to legend placement and plot margins to prevent overlaps on smaller screens.
    *   **Legend Position:** For legends, consider placing them horizontally at the bottom of the plot using `fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.8, xanchor="center", x=0.5))`.
    *   **Bottom Margin:** Adjust the bottom margin to provide sufficient space for the legend and x-axis title using `fig.update_layout(margin=dict(b=200))`. These values (`y` and `b`) may need fine-tuning based on the specific plot and content.

---

## 5. Good Code Style Practices

This section outlines practices for writing visually appealing and maintainable Python code, adhering to established programming standards like PEP 8.

### 5.1 General Code Aesthetics and Programming Standards (PEP 8)

Adhering to PEP 8 ensures your Python code is readable, consistent, and easier to collaborate on.

*   **Indentation**: Use 4 consecutive spaces for indentation. Prefer spaces over tabs.
*   **Maximum Line Length**: Limit all lines to a maximum of 79 characters. For docstrings and comments, the limit is 72 characters. Use implied line continuation (parentheses, brackets, braces) for long lines.
*   **Blank Lines**:
    *   Surround top-level function and class definitions with two blank lines.
    *   Surround method definitions inside classes with a single blank line.
    *   Use blank lines sparingly within functions to indicate logical sections.
*   **Naming Conventions**:
    *   Use `snake_case` for variable and function names.
    *   Use `CamelCase` for class names.
    *   Avoid single-character names unless they are for temporary or looping variables.
*   **Comments**:
    *   Use comments to explain *why* a certain line of code is necessary, rather than *what* it does.
    *   Limit comment and docstring line length to 72 characters.
    *   Use inline comments sparingly, separating them from the statement by two or more spaces.
*   **Readability**: Prioritize explicit and straightforward code. Avoid overly complex one-liners.
*   **One Statement Per Line**: Avoid placing multiple disjointed statements on the same line.

### 5.2 Import Organization

PEP 8 provides clear guidelines for organizing imports to enhance readability and prevent naming conflicts.

*   **Placement**: Imports should always be placed at the top of the file, just after any module comments and docstrings, and before module globals and constants.
*   **Grouping Order**: Imports should be grouped in the following order, with a blank line between each group:
    1.  Standard library imports (e.g., `os`, `sys`, `math`).
    2.  Related third-party imports (e.g., `numpy`, `pandas`, `requests`).
    3.  Local application/library-specific imports.
    Within each group, imports should be sorted in ascending order of their **full statement length (total character count of the line, excluding leading whitespace/indentation)**. For example:
    ```python
    # Incorrect (alphabetical)
    import os
    import sys

    # Correct (length-wise)
    import os  # 8 chars
    import sys # 9 chars
    ```
    ```python
    # Incorrect (alphabetical)
    import plotly.express as px # 26 chars
    import streamlit as st      # 22 chars

    # Correct (length-wise)
    import streamlit as st      # 22 chars
    import plotly.express as px # 26 chars
    ```
*   **Absolute vs. Relative Imports**: Absolute imports are generally recommended for readability and better error messages.
*   **Avoid Wildcard Imports**: Do not use `from <module> import *`. This makes it unclear which names are present in the namespace.
*   **One Import Per Line**: It is generally recommended to use one import statement per module.
    *   *Correct*:
        ```python
        import os
        import sys
        ```
    *   *Less Recommended*:
        ```python
        import os, sys
        ```
*   **Specific Imports**:
    *   For local modules (e.g., within `src/` directory), prefer `from src import module_name`. This allows direct access to `module_name.item`.
    *   If a third-party module is used extensively throughout the file, or its name is short and clear, prefer `import module` (Option 2).
    *   If a third-party module name is very long, prefer `import module as alias` (Option 4).
    *   If only a few specific items are needed from a module (local or third-party):
        *   If the single-line `from module import item1, item2, ...` statement fits within 79 characters, use it.
        *   If the single-line `from module import item1, item2, ...` statement would exceed 79 characters, then import each item on a separate line (e.g., `from module import item1`, `from module import item2`).
*   **Avoid Brackets in Imports**: Do not use parentheses `()` for multiline import statements.

### 5.3 Tools for Enforcement

Several tools can help automate the enforcement of these coding standards:

*   **Linters** (e.g., `flake8`, `pylint`): Analyze code for programmatic and stylistic errors, including PEP 8 violations.
*   **Formatters** (e.g., `Black`, `autopep8`, `YAPF`): Automatically reformat code to comply with style guides.
*   **Import Organizers** (e.g., `isort`): Automatically sort and group imports according to PEP 8 guidelines.

### 5.4 Documentation Aesthetics

Beyond just content, the visual presentation of documentation significantly impacts its readability and user experience. Adhering to these principles ensures documentation is not only informative but also visually appealing.

*   **Consistent Formatting**: Maintain a consistent style for headings, lists, code blocks, and emphasis (bold, italics) throughout all documentation. This creates a predictable and professional look.
*   **Clear and Concise Language**: Use plain, unambiguous language. Avoid jargon where simpler terms suffice. Break down complex ideas into smaller, digestible sentences and paragraphs.
*   **Use of Markdown Features**: Leverage Markdown's capabilities to structure content effectively:
    *   **Headings**: Use `##`, `###`, etc., to create a clear hierarchy of information.
    *   **Lists**: Use bullet points (`*` or `-`) or numbered lists (`1.`, `2.`) for sequential or itemized information.
    *   **Code Blocks**: Use triple backticks (```) for code examples to ensure proper formatting and readability.
    *   **Emphasis**: Use `*italics*` or `**bold**` for highlighting key terms or phrases.
*   **Whitespace and Line Breaks**: Use blank lines to separate paragraphs, sections, and code blocks. This improves scanning and reduces visual clutter.
*   **Examples and Visuals**: Where appropriate, include clear code examples, diagrams, or screenshots to illustrate concepts. For code examples, ensure they are well-formatted and directly relevant.
*   **Table of Contents**: For longer documents, include a table of contents to help users navigate quickly.
*   **Review and Refine**: Regularly review documentation for clarity, accuracy, and visual appeal. Get feedback from others to identify areas for improvement.