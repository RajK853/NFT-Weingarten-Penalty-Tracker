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
    ratio_df["Goal-to-Miss Ratio"] = ratio_df["Goals"] / ratio_df["Misses"]
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
    daily_performance["Goal-to-Miss Ratio"] = daily_performance["Goals"] / daily_performance["Misses"]
    daily_performance["Goal-to-Miss Ratio"] = daily_performance["Goal-to-Miss Ratio"].fillna(0) # Handle division by zero

    return daily_performance

def get_shoot_position_goals(data, player_name):
    player_goals = data[(data["Shooter Name"] == player_name) & (data["Status"] == "goal")]
    shoot_position_counts = player_goals["Shoot Position"].value_counts().reset_index()
    shoot_position_counts.columns = ["Shoot Position", "Goal Count"]
    return shoot_position_counts

def main():
    st.title("Penalty Shootout Dashboard")
    data = load_data()
    
    st.subheader("Top 10 Players by Goal-to-Miss Ratio")
    top_10_players = calculate_goal_miss_ratio(data).head(10)
    st.dataframe(top_10_players)
    
    # Phase 3: Interactive Dashboard Development
    st.sidebar.header("Player Selection")
    player_names = data["Shooter Name"].unique()
    selected_player = st.sidebar.selectbox("Select a Player", player_names)
    
    if selected_player:
        st.subheader(f"{selected_player}'s Performance Over Time")
        player_performance = get_player_performance_over_time(data, selected_player)
        fig_performance = px.line(player_performance, x="Date", y="Goal-to-Miss Ratio", title=f"{selected_player}'s Goal-to-Miss Ratio Over Time")
        st.plotly_chart(fig_performance)
        
        st.subheader(f"{selected_player}'s Goal Distribution by Shoot Position")
        shoot_position_goals = get_shoot_position_goals(data, selected_player)
        fig_positions = px.bar(shoot_position_goals, x="Shoot Position", y="Goal Count", title=f"{selected_player}'s Goal Distribution by Shoot Position")
        st.plotly_chart(fig_positions)
    
    st.subheader("Raw Data")
    st.dataframe(data)

if __name__ == "__main__":
    main()
