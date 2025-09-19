import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils import load_data, get_overall_shoot_position_success, get_goal_post_distribution_percentages, Constants

st.set_page_config(
    page_title="NFT Weingarten - Shot Distribution",
)

st.title("Shot Distribution Analysis")
st.markdown(
        """
        This page visualizes the effectiveness of different shoot positions and the individual goal distribution of players.
        """
    )

data = load_data()

st.subheader("Overall Shoot Position Effectiveness")
num_months_filter_position = st.slider("Filter for recent N months for Shoot Position Effectiveness", 1, 12, 12, key="shoot_position_months")
shoot_position_success = get_overall_shoot_position_success(data, num_months=num_months_filter_position)
fig_position_success = px.bar(shoot_position_success, x=shoot_position_success.index, y=Constants.GOAL_PERCENTAGE_COL,
                                title=f"Overall Goal Percentage by Shoot Position (Recent {num_months_filter_position} Months)",
                                hover_data=[Constants.GOALS_COL, Constants.TOTAL_SHOTS_COL])
fig_position_success.update_layout(yaxis_title="Goal Percentage (%)", yaxis_range=[0, 100])
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

if data.empty:
    st.warning("No data available to display player distribution.")
    individual_player_names = []
    selected_individual_player = None
else:
    individual_player_names = data[Constants.SHOOTER_NAME_COL].unique()
    selected_individual_player = st.sidebar.selectbox("Select a Player for Goal Distribution", individual_player_names, key="individual_player_selection")

if selected_individual_player:
    st.subheader(f"{selected_individual_player}'s Goal Distribution by Shoot Position")
    
    DECIMAL_POINTS = 0
    grid_percentages = get_goal_post_distribution_percentages(data, selected_individual_player, decimal_points=DECIMAL_POINTS)

    valid_percentages = [p for p in grid_percentages.values() if p > 0.0]
    if valid_percentages:
        min_percentage = min(valid_percentages)
        max_percentage = max(valid_percentages)
    else:
        min_percentage = 0.0
        max_percentage = 100.0 # Default if no valid percentages

    # Create the goal post visualization
    fig = go.Figure()

    # Goal post dimensions
    post_width = 50
    goal_width = 500
    goal_height = 400

    # Add goal post lines for left, top, and right edges
    fig.add_shape(type="line",
                  x0=0, y0=0, x1=0, y1=goal_height,
                  line=dict(color="white", width=post_width)) # Left post
    fig.add_shape(type="line",
                  x0=0, y0=goal_height, x1=goal_width, y1=goal_height,
                  line=dict(color="white", width=post_width)) # Top crossbar
    fig.add_shape(type="line",
                  x0=goal_width, y0=0, x1=goal_width, y1=goal_height,
                  line=dict(color="white", width=post_width)) # Right post
    
    # Add percentages as text annotations
    for r in range(3):
        for c in range(3):
            percentage = grid_percentages.get((r, c), 0.0)
            
            if percentage > 0.0: # Only draw if percentage is greater than 0.0
                x_pos = (c + 0.5) * goal_width / 3
                y_pos = (2.3 - r) * goal_height / 3 # Invert y-axis for display (row 0 is top)
                
                # Scale font size based on percentage
                font_size = 12 + (percentage / 100) * 20

                # Normalize percentage for relative scoring
                if max_percentage > min_percentage:
                    normalized_percentage = (percentage - min_percentage) / (max_percentage - min_percentage)
                else:
                    normalized_percentage = 0.0 # If all valid percentages are the same, treat as low for now

                # Scale color based on normalized percentage (red-to-green gradient) with darker shades
                min_color_val = 50  # Minimum RGB component value
                max_color_val = 200 # Maximum RGB component value
                color_range = max_color_val - min_color_val

                red_component = int(min_color_val + color_range * (1 - normalized_percentage))
                green_component = int(min_color_val + color_range * normalized_percentage)
                color = f"rgb({red_component}, {green_component}, 0)"
                
                # Scale marker size based on percentage
                marker_size = 30 + (percentage / 100) * 80

                fig.add_trace(go.Scatter(
                    x=[x_pos], y=[y_pos],
                    mode='markers+text',
                    marker=dict(size=marker_size, color=color, symbol='circle', opacity=0.7),
                    text=[f"{percentage:.{DECIMAL_POINTS}f}%"],
                    textfont=dict(size=font_size, color='white'), # Text color on marker
                    textposition='middle center',
                    showlegend=False
                ))

    # Update layout
    fig.update_layout(
        xaxis=dict(visible=False, range=[0, goal_width]),
        yaxis=dict(visible=False, range=[0, goal_height]),
        showlegend=False,
        width=goal_width + post_width, # Add some padding
        height=goal_height + post_width,
    )

    st.plotly_chart(fig, use_container_width=True)
