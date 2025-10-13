"""
Streamlit page for explaining the scoring system.
"""

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

from src import ui
from src.constants import Scoring, UI

ui.setup_page(
    page_icon="ℹ️",
    page_title="NFT Weingarten - Scoring Method",
    page_description="""This page explains our fair scoring system for players and goalkeepers, showing who is playing well right now.""",
    render_logo=True,
)


st.header("Base Points System")

st.markdown("Players get points for each penalty outcome:")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Shooter Scoring")
    player_scoring_data = {
        "Outcome": ["Goal", "Saved by Goalkeeper", "Missed (Out)"],
        "Points": [Scoring.GOAL, Scoring.SAVED, Scoring.OUT],
    }
    player_scoring_df = pd.DataFrame(player_scoring_data)
    st.dataframe(player_scoring_df, hide_index=True, width="stretch")

with col2:
    st.subheader("Goalkeeper Scoring")
    keeper_scoring_data = {
        "Outcome": ["Goal Conceded", "Penalty Saved", "Shooter Missed (Out)"],
        "Points": [Scoring.KEEPER_GOAL, Scoring.KEEPER_SAVED, Scoring.KEEPER_OUT],
    }
    keeper_scoring_df = pd.DataFrame(keeper_scoring_data)
    st.dataframe(keeper_scoring_df, hide_index=True, width="stretch")


st.header("Time-Weighted Scoring: Recent Games Matter More")

st.markdown(
    f"Recent games are more important for the score than older games, helping us see who is in good form now. This is called **time-weighted scoring**. A score's value is cut in half every **{Scoring.PERFORMANCE_HALF_LIFE_DAYS} days** (its **half-life**). For example, a penalty from today is worth double the points of a penalty from {Scoring.PERFORMANCE_HALF_LIFE_DAYS} days ago."
)
with st.expander("See the Math: The Half-Life Formula"):
    st.markdown(
        f"""
The score's value over time is calculated using the formula:

`Weighted Score = Original Score * 2^(-days_ago / half_life)`

This formula reduces the score's value by half for each half-life period. Our app uses a half-life of **{Scoring.PERFORMANCE_HALF_LIFE_DAYS} days**. The chart below demonstrates this; adjust the **"Simulation"** to observe how different half-life values impact the score.
"""
    )

    # --- Interactive Inputs ---
    col1, col2 = st.columns(2)
    with col1:
        original_score_input = st.number_input(
            "Original Score", value=3.0, step=0.5, key="sim_score"
        )
    with col2:
        sim_half_life_input = st.number_input(
            "Simulation Half-Life (in days)",
            value=30.0,
            min_value=1.0,
            step=1.0,
            format="%.1f",
            key="sim_half_life",
        )

    # --- Plot Generation ---
    days_range = np.arange(0, 366)

    # --- Current Setting Data ---
    setting_scores = original_score_input * (
        2 ** (-days_range / Scoring.PERFORMANCE_HALF_LIFE_DAYS)
    )
    setting_df = pd.DataFrame(
        {
            "Days Ago": days_range,
            "Weighted Score": setting_scores,
            "Curve": "Current Setting",
        }
    )

    # --- Simulation Data ---
    simulation_scores = original_score_input * (
        2 ** (-days_range / sim_half_life_input)
    )
    simulation_df = pd.DataFrame(
        {
            "Days Ago": days_range,
            "Weighted Score": simulation_scores,
            "Curve": "Simulation",
        }
    )

    # --- Combine and Plot ---
    combined_df = pd.concat([setting_df, simulation_df])
    fig = px.line(
        combined_df,
        x="Days Ago",
        y="Weighted Score",
        color="Curve",
        line_dash="Curve",
        title="Decay Curve Comparison",
        line_dash_map={"Current Setting": "dash", "Simulation": "solid"},
    )

    # --- Add Half-Life Markers ---
    # Current Setting Half-Life
    fig.add_scatter(
        x=[Scoring.PERFORMANCE_HALF_LIFE_DAYS],
        y=[original_score_input / 2],
        mode="markers",
        marker=dict(size=10, symbol="x-dot", color="blue"),
        name=f"Current Half-Life ({Scoring.PERFORMANCE_HALF_LIFE_DAYS:.1f} days)",
    )

    # Simulation Half-Life
    fig.add_scatter(
        x=[sim_half_life_input],
        y=[original_score_input / 2],
        mode="markers",
        marker=dict(size=10, symbol="x-dot", color="red"),
        name=f"Simulated Half-Life ({sim_half_life_input:.1f} days)",
    )

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,  # Adjusted to be closer to the plot
            xanchor="center",
            x=0.5,
        ),
    )
    ui.render_plotly_chart(fig, st_width_mode="stretch", fixed_range=True)

st.info(
    """
**How is the final score calculated?**

We add up all the weighted scores for each player or goalkeeper to get their total score.
"""
)
