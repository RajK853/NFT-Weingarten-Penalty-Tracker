"""
Streamlit page for explaining the scoring system.
"""
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from src.constants import Scoring

st.set_page_config(
    page_title="NFT Weingarten - Scoring Information",
    page_icon="ℹ️",
    initial_sidebar_state="expanded",
    layout="wide"
)

st.title("How Scoring Works")

st.markdown("""
This page explains how we score players and goalkeepers. 
We want a fair system that shows who is playing well right now.
""")

st.header("Base Points System")

st.markdown("Players get points for each penalty outcome:")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Shooter Scoring")
    player_scoring_data = {
        'Outcome': ['Goal', 'Saved by Goalkeeper', 'Missed (Out)'],
        'Points': [Scoring.GOAL, Scoring.SAVED, Scoring.OUT]
    }
    player_scoring_df = pd.DataFrame(player_scoring_data)
    st.dataframe(player_scoring_df, hide_index=True, use_container_width=True)

with col2:
    st.subheader("Goalkeeper Scoring")
    keeper_scoring_data = {
        'Outcome': ['Goal Conceded', 'Penalty Saved', 'Shooter Missed (Out)'],
        'Points': [Scoring.KEEPER_GOAL, Scoring.KEEPER_SAVED, Scoring.KEEPER_OUT]
    }
    keeper_scoring_df = pd.DataFrame(keeper_scoring_data)
    st.dataframe(keeper_scoring_df, hide_index=True, use_container_width=True)


st.header("Time-Weighted Scoring: Recent Games Matter More")

st.markdown(f"""
Recent games are more important for the score than older games. This helps us see who is in good form now. We call this **time-weighted scoring**.

A score's value is cut in half every **{Scoring.PERFORMANCE_HALF_LIFE_DAYS} days**. This is called the **half-life**. 
For example, a penalty from today is worth double the points of a penalty from {Scoring.PERFORMANCE_HALF_LIFE_DAYS} days ago.
""")

with st.expander("See the Math: The Half-Life Formula"):
    st.markdown(f"""
    We use this formula to calculate the score's value over time:

    `Weighted Score = Original Score * 2^(-days_ago / half_life)`

    This formula reduces the score's value by half for each half-life period. Our app uses a half-life of **{Scoring.PERFORMANCE_HALF_LIFE_DAYS} days**.

    You can use the chart below to see how this works. Change the **"Simulation"** to see how different half-life values affect the score.
    """)

    # --- Interactive Inputs ---
    col1, col2 = st.columns(2)
    with col1:
        original_score_input = st.number_input("Original Score", value=3.0, step=0.5, key="sim_score")
    with col2:
        sim_half_life_input = st.number_input("Simulation Half-Life (in days)", value=30.0, min_value=1.0, step=1.0, format="%.1f", key="sim_half_life")

    # --- Plot Generation ---
    days_range = np.arange(0, 366)

    # --- Current Setting Data ---
    setting_scores = original_score_input * (2 ** (-days_range / Scoring.PERFORMANCE_HALF_LIFE_DAYS))
    setting_df = pd.DataFrame({
        'Days Ago': days_range,
        'Weighted Score': setting_scores,
        'Curve': "Current Setting"
    })

    # --- Simulation Data ---
    simulation_scores = original_score_input * (2 ** (-days_range / sim_half_life_input))
    simulation_df = pd.DataFrame({
        'Days Ago': days_range,
        'Weighted Score': simulation_scores,
        'Curve': 'Simulation'
    })

    # --- Combine and Plot ---
    combined_df = pd.concat([setting_df, simulation_df])
    fig = px.line(
        combined_df,
        x='Days Ago',
        y='Weighted Score',
        color='Curve',
        line_dash='Curve',
        title='Decay Curve Comparison',
        line_dash_map={"Current Setting": "dash", "Simulation": "solid"}
    )

    # --- Add Half-Life Markers ---
    # Current Setting Half-Life
    fig.add_scatter(x=[Scoring.PERFORMANCE_HALF_LIFE_DAYS], y=[original_score_input/2], mode='markers', marker=dict(size=10, symbol="x-dot", color='blue'), name=f"Current Half-Life ({Scoring.PERFORMANCE_HALF_LIFE_DAYS:.1f} days)")

    # Simulation Half-Life
    fig.add_scatter(x=[sim_half_life_input], y=[original_score_input/2], mode='markers', marker=dict(size=10, symbol="x-dot", color='red'), name=f"Simulated Half-Life ({sim_half_life_input:.1f} days)")

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.8, # Even more negative
            xanchor="center",
            x=0.5
        ),
        margin=dict(b=200) # Even more increased bottom margin
    )

    st.plotly_chart(fig, use_container_width=True)

st.info("""
**How is the final score calculated?**

We add up all the weighted scores for each player or goalkeeper to get their total score.
""")