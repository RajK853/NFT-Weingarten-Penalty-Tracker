import streamlit as st
import pandas as pd
import plotly.express as px

def load_data():
    data = pd.read_csv("data/penalty.csv")
    return data

def calculate_goal_miss_ratio(data):
    goals = data[data["Status"] == "goal"].groupby("Shooter Name").size()
    misses = data[data["Status"] != "goal"].groupby("Shooter Name").size()
    
    ratio_df = pd.DataFrame({
        "Goals": goals,
        "Misses": misses
    }).fillna(0)
    
    ratio_df["Misses"] = ratio_df["Misses"].astype(int)
    ratio_df["Total Shots"] = ratio_df["Goals"] + ratio_df["Misses"]
    ratio_df["Goal-to-Miss Ratio"] = (ratio_df["Goals"] / ratio_df["Total Shots"]) * 100
    ratio_df["Goal-to-Miss Ratio"] = ratio_df["Goal-to-Miss Ratio"].fillna(0) # Handle division by zero
    
    return ratio_df.sort_values(by="Goal-to-Miss Ratio", ascending=False)

def get_player_performance_over_time(data, player_name):
    player_data = data[data["Shooter Name"] == player_name].copy()
    player_data["Date"] = pd.to_datetime(player_data["Date"])

    # Calculate goals and misses per date
    daily_performance = player_data.groupby("Date").apply(lambda x: pd.Series({
        "Goals": (x["Status"] == "goal").sum(),
        "Misses": (x["Status"] != "goal").sum()
    })).reset_index()

    daily_performance["Total Shots"] = daily_performance["Goals"] + daily_performance["Misses"]
    daily_performance["Goal-to-Miss Ratio"] = (daily_performance["Goals"] / daily_performance["Total Shots"]) * 100
    daily_performance["Goal-to-Miss Ratio"] = daily_performance["Goal-to-Miss Ratio"].fillna(0) # Handle division by zero

    return daily_performance

def get_shoot_position_goals(data, player_name):
    player_goals = data[(data["Shooter Name"] == player_name) & (data["Status"] == "goal")]
    shoot_position_counts = player_goals["Shoot Position"].value_counts().reset_index()
    shoot_position_counts.columns = ["Shoot Position", "Goal Count"]
    return shoot_position_counts

def get_shoot_position_goals(data, player_name):
    player_goals = data[(data["Shooter Name"] == player_name) & (data["Status"] == "goal")]
    shoot_position_counts = player_goals["Shoot Position"].value_counts().reset_index()
    shoot_position_counts.columns = ["Shoot Position", "Goal Count"]
    return shoot_position_counts

def get_player_status_counts_over_time(data, selected_players):
    if not selected_players:
        return pd.DataFrame() # Return empty DataFrame if no players selected

    filtered_data = data[data["Shooter Name"].isin(selected_players)].copy()
    filtered_data["Date"] = pd.to_datetime(filtered_data["Date"])

    # Count occurrences of each status for each player per day
    status_counts = filtered_data.groupby(["Date", "Shooter Name", "Status"]).size().reset_index(name="Count")

    # Ensure all statuses are present for each date and player for consistent plotting
    from itertools import product
    all_dates = filtered_data["Date"].unique()
    all_statuses = filtered_data["Status"].unique()
    
    # Create a complete grid of all combinations
    idx = pd.MultiIndex.from_product([all_dates, selected_players, all_statuses], names=["Date", "Shooter Name", "Status"])
    full_df = pd.DataFrame(index=idx).reset_index()

    # Merge with actual counts, filling missing with 0
    status_counts_full = pd.merge(full_df, status_counts, on=["Date", "Shooter Name", "Status"], how="left").fillna(0)
    status_counts_full["Count"] = status_counts_full["Count"].astype(int)

    return status_counts_full.sort_values(by=["Date", "Shooter Name", "Status"])

def main():
    st.set_page_config(page_title="NFT Weingarten - Penalty Tracker")
    col1, col2 = st.columns([1, 4]) # Adjust column width as needed
    with col1:
        st.image("data/logo.jpg", width=100)
    with col2:
        st.title("NFT Weingarten - Penalty Tracker")
    data = load_data()
    
    st.subheader("Top 10 Players by Goal-to-Miss Ratio")
    top_10_players = calculate_goal_miss_ratio(data).head(10)
    fig_top_players = px.bar(top_10_players, x=top_10_players.index, y="Goal-to-Miss Ratio", title="Top 10 Players by Goal Percentage")
    st.plotly_chart(fig_top_players)
    
    # Player Selection for Performance Over Time
    st.subheader("Compare Player Performance Over Time")
    player_names = data["Shooter Name"].unique()
    selected_players = st.multiselect("Select up to 5 Players to Compare", player_names, default=player_names[:2], max_selections=5)
    
    if selected_players:
        st.subheader(f"Performance Over Time")
        player_status_data = get_player_status_counts_over_time(data, selected_players)
        
        if not player_status_data.empty:
            # Create separate charts for each status
            status_colors = {"goal": "green", "saved": "orange", "out": "red"}

            for status, color in status_colors.items():
                status_df = player_status_data[player_status_data["Status"] == status]
                if not status_df.empty:
                    fig = px.scatter(status_df,
                                  x="Date",
                                  y="Count",
                                  color="Shooter Name",
                                  size=[8]*len(status_df), # Fixed size for all points
                                  title=status.title())
                    st.plotly_chart(fig)
                else:
                    st.info(f"No {status} data to display for selected players.")

    # Individual Player Goal Distribution (remains in sidebar for now, or can be moved)
    st.sidebar.header("Individual Player Analysis")
    individual_player_names = data["Shooter Name"].unique()
    selected_individual_player = st.sidebar.selectbox("Select a Player for Goal Distribution", individual_player_names)
    
    if selected_individual_player:
        st.subheader(f"{selected_individual_player}'s Goal Distribution by Shoot Position")
        shoot_position_goals = get_shoot_position_goals(data, selected_individual_player)
        fig_positions = px.bar(shoot_position_goals, x="Shoot Position", y="Goal Count", title=f"{selected_individual_player}'s Goal Distribution by Shoot Position")
        st.plotly_chart(fig_positions)

if __name__ == "__main__":
    main()
