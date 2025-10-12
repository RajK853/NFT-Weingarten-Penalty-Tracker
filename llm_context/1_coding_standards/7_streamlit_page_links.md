# Streamlit Page Link Usage

For internal navigation within the Streamlit application, always prefer `st.page_link` over traditional markdown links.

## Reasoning:
- **Safety:** `st.page_link` provides a safer way to navigate within the Streamlit application, preventing potential security vulnerabilities associated with raw markdown links.
- **User Experience:** Markdown links often open in a new browser tab, which can disrupt the user's flow and create a less cohesive application experience. `st.page_link` ensures that internal navigation happens within the same tab, maintaining a consistent user experience.
- **Streamlit Integration:** `st.page_link` is designed to work seamlessly with Streamlit's page management, offering better integration and control over navigation.

## Example:
Instead of:
```python
st.markdown("Please visit the [Scoring Method](/Scoring_Method) page.")
```

Use:
```python
st.page_link("pages/3_Scoring_Method.py", label="Please visit the Scoring Method page.")
```
