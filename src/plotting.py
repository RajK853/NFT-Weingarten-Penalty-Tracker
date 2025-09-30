import pandas as pd
import plotly.graph_objects as go
from src.constants import Columns, Data, GoalVisual, Status, UI

def create_shot_distribution_chart(data: pd.DataFrame) -> go.Figure:
    """
    Creates a scatter plot of shot distribution on a goalpost visual.

    Args:
        data (pd.DataFrame): The input DataFrame containing penalty shootout data
                             with 'Shot_X', 'Shot_Y', and 'Status' columns.

    Returns:
        go.Figure: A Plotly Graph Object figure displaying the shot distribution.
    """
    fig = go.Figure()

    # Draw the goalpost (simplified rectangle)
    fig.add_shape(
        type="rect",
        x0=0, y0=0, x1=GoalVisual.GOAL_WIDTH, y1=GoalVisual.GOAL_HEIGHT,
        line=dict(color=GoalVisual.GOAL_POST_COLOR, width=GoalVisual.GOAL_POST_LINE_WIDTH),
        fillcolor=GoalVisual.PITCH_COLOR
    )

    # Add scatter points for each shot
    # Assuming Shot_X and Shot_Y are normalized or within the GOAL_WIDTH/GOAL_HEIGHT range
    fig.add_trace(go.Scatter(
        x=data[Columns.SHOT_X],
        y=data[Columns.SHOT_Y],
        mode='markers',
        marker=dict(
            size=UI.PLOTLY_SCATTER_MARKER_SIZE,
            color=data[Columns.STATUS].map({
                Status.GOAL: UI.COLOR_GREEN,
                Status.SAVED: UI.COLOR_BLUE,
                Status.OUT: UI.COLOR_RED
            }),
            opacity=UI.PLOTLY_SCATTER_MARKER_OPACITY
        ),
        text=data.apply(lambda row: f"Shooter: {row[Columns.SHOOTER_NAME]}<br>Outcome: {row[Columns.STATUS]}", axis=1),
        hoverinfo='text'
    ))

    fig.update_layout(
        title="Shot Distribution on Goal",
        xaxis=dict(range=[Data.DEFAULT_FILL_VALUE, GoalVisual.GOAL_WIDTH], showgrid=UI.PLOTLY_AXIS_SHOWGRID, zeroline=UI.PLOTLY_AXIS_ZEROLINE, visible=UI.PLOTLY_AXIS_VISIBLE),
        yaxis=dict(range=[Data.DEFAULT_FILL_VALUE, GoalVisual.GOAL_HEIGHT], showgrid=UI.PLOTLY_AXIS_SHOWGRID, zeroline=UI.PLOTLY_AXIS_ZEROLINE, visible=UI.PLOTLY_AXIS_VISIBLE),
        plot_bgcolor=UI.PLOTLY_BG_COLOR_TRANSPARENT, # Make plot background transparent to show pitch color
        showlegend=UI.PLOTLY_SHOW_LEGEND,
        width=UI.GOAL_POST_WIDTH_VISUAL,
        height=UI.GOAL_POST_HEIGHT_VISUAL
    )

    return fig
