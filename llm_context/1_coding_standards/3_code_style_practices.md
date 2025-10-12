# Good Code Style Practices

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
    *   **Internal Functions/Methods (Leading Underscore):** Use a single leading underscore (e.g., `_internal_function`) for functions, methods, or variables that are intended for internal use within a module or class. This is a convention to signal that these are not part of the public API and should not be accessed directly from outside the defining scope. It aids in clarity, API stability, and avoids accidental naming collisions.
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