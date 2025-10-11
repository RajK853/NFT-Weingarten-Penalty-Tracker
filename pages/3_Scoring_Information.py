"""
Streamlit page for explaining the scoring system.
"""
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from src.constants import UI, Scoring

st.set_page_config(
    page_title="NFT Weingarten - Scoring Information",
    page_icon="ℹ️",
    initial_sidebar_state="expanded",
    layout="wide"
)

st.title("Scoring Information")

st.header("Player Scoring System")
player_scoring_data = {
    'Outcome': ['Goal', 'Saved', 'Out'],
    'Points': [Scoring.GOAL, Scoring.SAVED, Scoring.OUT]
}
player_scoring_df = pd.DataFrame(player_scoring_data)
st.dataframe(player_scoring_df, hide_index=True)

st.header("Goalkeeper Scoring System")
keeper_scoring_data = {
    'Outcome': ['Goal', 'Saved', 'Out'],
    'Points': [Scoring.KEEPER_GOAL, Scoring.KEEPER_SAVED, Scoring.KEEPER_OUT]
}
keeper_scoring_df = pd.DataFrame(keeper_scoring_data)
st.dataframe(keeper_scoring_df, hide_index=True)

st.header("Time-Weighted Scoring")
st.write(f"""
To better reflect the current form of players and goalkeepers, a time-weighted scoring system is used. This means that more recent performances have a greater impact on the score than older performances.

The weight of each performance decreases exponentially over time, with a half-life of **{Scoring.PERFORMANCE_HALF_LIFE_DAYS} days**. This means that a performance from {Scoring.PERFORMANCE_HALF_LIFE_DAYS} days ago is worth half as much as a performance from today.
""")

with st.expander("How is the Time-Weighted Score Calculated?"):
        st.markdown("""
        To better reflect a player's current form, scores are weighted based on how recently they occurred. This is done using an **exponential decay** model, where the weight of a score decreases as it gets older.

        The formula used is:
        ```
        Weighted Score = Original Score * e^(-decay_rate * days_ago)
        ```
        The `decay_rate` is what controls how quickly the score value decreases. For simplicity, we configure this using a "half-life" value (currently **{Scoring.PERFORMANCE_HALF_LIFE_DAYS} days**), which is then converted to a decay rate for the actual leaderboard calculations.
        """)
        st.markdown("--- ")
        st.subheader("Decay Curve Comparison")
        st.markdown("Adjust the parameters for the **Simulation** curve (solid line) and compare it to the application's **Current Setting** (dashed line).")

        # --- Interactive Inputs ---
        col1, col2 = st.columns(2)
        with col1:
            original_score_input = st.number_input("Original Score", value=1.5, step=0.5, key="sim_score")
        with col2:
            decay_rate_input = st.number_input("Simulation Decay Rate", value=0.020, min_value=0.0, step=0.005, format="%.3f", key="sim_decay")

        # --- Plot Generation ---
        days_range = np.arange(0, 366)

        # --- Current Setting Data ---
        setting_scores = original_score_input * np.exp(-Scoring.DECAY_RATE * days_range)
        setting_df = pd.DataFrame({
            'Days Ago': days_range,
            'Weighted Score': setting_scores,
            'Curve': "Current Setting"
        })

        # --- Simulation Data ---
        simulation_scores = original_score_input * np.exp(-decay_rate_input * days_range)
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
        if Scoring.DECAY_RATE > 0:
            setting_half_life = np.log(2) / Scoring.DECAY_RATE
            fig.add_scatter(x=[setting_half_life], y=[original_score_input/2], mode='markers', marker=dict(size=10, color='blue'), name=f"Current Setting Half-Life ({setting_half_life:.1f} days)")

        # Simulation Half-Life
        if decay_rate_input > 0:
            sim_half_life = np.log(2) / decay_rate_input
            fig.add_scatter(x=[sim_half_life], y=[original_score_input/2], mode='markers', marker=dict(size=10, color='red'), name=f"Simulation Half-Life ({sim_half_life:.1f} days)")

        st.plotly_chart(fig, use_container_width=True)
