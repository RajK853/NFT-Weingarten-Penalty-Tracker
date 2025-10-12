# Plotting Best Practices (Streamlit & Plotly)

To ensure a consistent and user-friendly experience across all devices, especially mobile, adhere to the following guidelines when creating plots with Plotly in Streamlit:

*   **Static Plots with Tooltips:** All plots should be static (no zooming or panning) but must retain hover tooltip information.
    *   **Fixed Range:** All plots should have `fixed_range=True` by default to prevent zooming and panning, ensuring a consistent view.
    *   **Disable Interactivity:** For each Plotly figure (`fig`), disable zooming and panning by adding `fig.update_layout(xaxis_fixedrange=True, yaxis_fixedrange=True)`.
    *   **Hide Mode Bar:** Always use `st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': UI.PLOTLY_DISPLAY_MODE_BAR})`. This hides the interactive mode bar (zoom, pan, etc.) while keeping tooltips active.
    *   **Import UI:** Ensure `UI` is imported from `src.constants` in any file where `UI.PLOTLY_DISPLAY_MODE_BAR` is used.
*   **Mobile-Friendly Layout:** Pay attention to legend placement and plot margins to prevent overlaps on smaller screens.
    *   **Legend Position:** For legends, consider placing them horizontally at the bottom of the plot using `fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.8, xanchor="center", x=0.5))`.
    *   **Bottom Margin:** Adjust the bottom margin to provide sufficient space for the legend and x-axis title using `fig.update_layout(margin=dict(b=200))`. These values (`y` and `b`) may need fine-tuning based on the specific plot and content.