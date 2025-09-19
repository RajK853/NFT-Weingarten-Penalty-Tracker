"""
Streamlit page for analyzing shot distribution in penalty shootouts.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils import load_data, get_overall_shoot_position_success, get_goal_post_distribution_percentages, Constants
from typing import List, Optional

st.set_page_config(
    page_title="NFT Weingarten - Shot Distribution",
)

st.title("Shot Distribution Analysis")
st.markdown(
        """
        This page visualizes the effectiveness of different shoot positions and the individual goal distribution of players.
        """
    )

data: pd.DataFrame = load_data()

st.subheader("Overall Shoot Position Effectiveness")
num_months_filter_position: int = st.slider("Filter for recent N months for Shoot Position Effectiveness", 
                                            Constants.SLIDER_MIN_MONTHS, Constants.SLIDER_MAX_MONTHS, Constants.SLIDER_DEFAULT_MONTHS, 
                                            key="shoot_position_months")
shoot_position_success: pd.DataFrame = get_overall_shoot_position_success(data, num_months=num_months_filter_position)
fig_position_success = px.bar(shoot_position_success, x=shoot_position_success.index, y=Constants.GOAL_PERCENTAGE_COL,
                                title=f"Overall Goal Percentage by Shoot Position (Recent {num_months_filter_position} Months)",
                                hover_data=[Constants.GOALS_COL, Constants.TOTAL_SHOTS_COL])
fig_position_success.update_layout(yaxis_title="Goal Percentage (%)", yaxis_range=[Constants.Y_AXIS_RANGE_MIN, Constants.Y_AXIS_RANGE_MAX])
fig_position_success.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
st.plotly_chart(fig_position_success)

st.subheader("Individual Player Goal Distribution")
st.markdown(
        """
        Explore the goal distribution of individual players based on their shoot positions.
        Select a player from the sidebar to see where they tend to aim their shots.
        """
    )
st.sidebar.header("Individual Player Analysis")

individual_player_names: List[str]
selected_individual_player: Optional[str]

if data.empty:
    st.warning("No data available to display player distribution.")
    individual_player_names = []
    selected_individual_player = None
else:
    individual_player_names = list(data[Constants.SHOOTER_NAME_COL].unique())
    selected_individual_player = st.sidebar.selectbox("Select a Player for Goal Distribution", individual_player_names, key="individual_player_selection")

if selected_individual_player:
    st.subheader(f"{selected_individual_player}'s Goal Distribution by Shoot Position")
    
    grid_percentages: dict = get_goal_post_distribution_percentages(data, selected_individual_player, decimal_points=Constants.DECIMAL_POINTS_DISPLAY)

    valid_percentages: List[float] = [p for p in grid_percentages.values() if p > 0.0]
    if valid_percentages:
        min_percentage: float = min(valid_percentages)
        max_percentage: float = max(valid_percentages)
    else:
        min_percentage = 0.0
        max_percentage = 100.0 # Default if no valid percentages

    # Create the goal post visualization
    fig = go.Figure()

    # Add goal post lines for left, top, and right edges
    fig.add_shape(type="line",
                  x0=0, y0=0, x1=0, y1=Constants.GOAL_POST_HEIGHT_VISUAL,
                  line=dict(color=Constants.GOAL_POST_COLOR, width=Constants.POST_LINE_WIDTH_VISUAL)) # Left post
    fig.add_shape(type="line",
                  x0=0, y0=Constants.GOAL_POST_HEIGHT_VISUAL, x1=Constants.GOAL_POST_WIDTH_VISUAL, y1=Constants.GOAL_POST_HEIGHT_VISUAL,
                  line=dict(color=Constants.GOAL_POST_COLOR, width=Constants.POST_LINE_WIDTH_VISUAL)) # Top crossbar
    fig.add_shape(type="line",
                  x0=Constants.GOAL_POST_WIDTH_VISUAL, y0=0, x1=Constants.GOAL_POST_WIDTH_VISUAL, y1=Constants.GOAL_POST_HEIGHT_VISUAL,
                  line=dict(color=Constants.GOAL_POST_COLOR, width=Constants.POST_LINE_WIDTH_VISUAL)) # Right post
    
    # Add percentages as text annotations
    for r in range(Constants.GRID_DIMENSION):
        for c in range(Constants.GRID_DIMENSION):
            percentage: float = grid_percentages.get((r, c), 0.0)
            
            if percentage > 0.0: # Only draw if percentage is greater than 0.0
                x_pos: float = (c + Constants.X_POS_OFFSET) * Constants.GOAL_POST_WIDTH_VISUAL / Constants.GRID_DIMENSION
                y_pos: float = (Constants.Y_POS_INVERT_FACTOR - r) * Constants.GOAL_POST_HEIGHT_VISUAL / Constants.GRID_DIMENSION # Invert y-axis for display (row 0 is top)
                
                # Scale font size based on percentage
                font_size: float = Constants.FONT_SIZE_BASE + (percentage / 100) * Constants.FONT_SIZE_SCALE

                # Normalize percentage for relative scoring
                if max_percentage > min_percentage:
                    normalized_percentage: float = (percentage - min_percentage) / (max_percentage - min_percentage)
                else:
                    normalized_percentage = 0.0 # If all valid percentages are the same, treat as low for now

                # Scale color based on normalized percentage (red-to-green gradient) with darker shades
                red_component: int = int(Constants.COLOR_MIN_RGB + (Constants.COLOR_MAX_RGB - Constants.COLOR_MIN_RGB) * (1 - normalized_percentage))
                green_component: int = int(Constants.COLOR_MIN_RGB + (Constants.COLOR_MAX_RGB - Constants.COLOR_MIN_RGB) * normalized_percentage)
                color: str = f"rgb({red_component}, {green_component}, 0)"
                
                # Scale marker size based on percentage
                marker_size: float = Constants.MARKER_SIZE_BASE + (percentage / 100) * Constants.MARKER_SIZE_SCALE

                fig.add_trace(go.Scatter(
                    x=[x_pos], y=[y_pos],
                    mode='markers+text',
                    marker=dict(size=marker_size, color=color, symbol='circle', opacity=0.7),
                    text=[f"{percentage:.{Constants.DECIMAL_POINTS_DISPLAY}f}%"],
                    textfont=dict(size=font_size, color='white'), # Text color on marker
                    textposition='middle center',
                    showlegend=False
                ))

    # Update layout
    fig.update_layout(
        xaxis=dict(visible=False, range=[0, Constants.GOAL_POST_WIDTH_VISUAL]),
        yaxis=dict(visible=False, range=[0, Constants.GOAL_POST_HEIGHT_VISUAL]),
        showlegend=False,
        width=Constants.GOAL_POST_WIDTH_VISUAL + Constants.POST_LINE_WIDTH_VISUAL, # Add some padding
        height=Constants.GOAL_POST_HEIGHT_VISUAL + Constants.POST_LINE_WIDTH_VISUAL,
    )

    st.plotly_chart(fig, use_container_width=True)