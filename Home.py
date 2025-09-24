import pandas as pd
import streamlit as st
import plotly.express as px
from utils import (
    load_data, get_overall_statistics, calculate_player_scores, 
    calculate_save_percentage, Constants, get_recent_penalties,
    get_longest_goal_streak, get_most_goals_in_session,
    get_most_saves_in_session, get_marathon_man, get_busiest_day, 
    get_biggest_rivalry
)

st.set_page_config(
    page_title="NFT Weingarten - Penalty Tracker",
    page_icon=Constants.EMOJI_HOME_PAGE,
    initial_sidebar_state="expanded",
    layout="wide"
)

# --- Header ---

col1, col2, col3 = st.columns([4,1,4])
with col2:
    st.image(Constants.LOGO_PATH, use_container_width=True)

st.markdown("<h1 style='text-align: center;'>NFT Weingarten Penalty Tracker</h1>", unsafe_allow_html=True)

st.markdown(
    """
    Welcome to the **NFT Weingarten Penalty Tracker**! This dashboard offers a deep dive into our penalty shootout data, providing a comprehensive overview of player performances, goalkeeper stats, and historical trends. 
    
    Whether you're a player looking to analyze your performance or a fan interested in the stats, this dashboard has something for you. Explore the different sections to uncover insights and celebrate the best moments of our penalty shootouts.
    """
)

st.markdown("---")

# --- Load Data ---
data = load_data()
if not data.empty:
    data[Constants.DATE_COL] = pd.to_datetime(data[Constants.DATE_COL]).dt.date

    # --- Main Content ---
    col_main1, col_main2 = st.columns(2, gap="large")

    with col_main1:


        with st.container(border=True):
            st.subheader("Hall of Fame")
            st.markdown("This section celebrates the most remarkable achievements and milestones in our penalty shootout history. Browse through the tabs to discover all-time records, single-session heroics, and fun facts about our players and games.")
            
            # Get records data
            longest_streak_player, longest_streak = get_longest_goal_streak(data)
            most_goals_player, most_goals_date, most_goals = get_most_goals_in_session(data)
            most_saves_keeper, most_saves_date, most_saves = get_most_saves_in_session(data)
            marathon_man, sessions = get_marathon_man(data)
            busiest_date, busiest_count = get_busiest_day(data)
            rival_shooter, rival_keeper, encounters = get_biggest_rivalry(data)

            tab1, tab2, tab3 = st.tabs(["🏆 All-Time Records", "📅 Single Session Records", "✨ Fun Facts"])

            with tab1:
                col1_tab1, col2_tab1 = st.columns(2)
                with col1_tab1:
                    st.metric(
                        label="🏆 Longest Goal Streak",
                        value=longest_streak_player,
                        delta=f"{longest_streak} goals",
                        help="The player with the most consecutive goals scored."
                    )
                with col2_tab1:
                    st.metric(
                        label="⚔️ Biggest Rivalry",
                        value=f"{rival_shooter} vs {rival_keeper}",
                        delta=f"{encounters} encounters",
                        help="The most frequent matchup between a shooter and a goalkeeper."
                    )

            with tab2:
                col1_tab2, col2_tab2 = st.columns(2)
                with col1_tab2:
                    st.metric(
                        label="⚽ Most Goals in a Session",
                        value=most_goals_player,
                        delta=f"{most_goals} goals on {most_goals_date}",
                        help="The player who scored the most goals in a single session."
                    )
                with col2_tab2:
                    st.metric(
                        label="🧤 Most Saves in a Session",
                        value=most_saves_keeper,
                        delta=f"{most_saves} saves on {most_saves_date}",
                        help="The goalkeeper who made the most saves in a single session."
                    )

            with tab3:
                col1_tab3, col2_tab3 = st.columns(2)
                with col1_tab3:
                    st.metric(
                        label="🏃 Marathon Man (Most Sessions)",
                        value=marathon_man,
                        delta=f"{sessions} sessions",
                        help="The player who has participated in the most penalty sessions."
                    )
                with col2_tab3:
                    st.metric(
                        label="🗓️ Busiest Day",
                        value=str(busiest_date),
                        delta=f"{busiest_count} penalties",
                        help="The date with the highest number of penalties taken."
                    )

    with col_main2:
        with st.container(border=True):
            st.subheader("Top Performers")
            st.markdown("This section highlights the player and goalkeeper who have shown exceptional performance in the last 30 days. It's a snapshot of who is currently in top form.")
            
            current_date = pd.to_datetime(data[Constants.DATE_COL]).max()
            start_date_top_performers = (current_date - pd.DateOffset(days=Constants.RECENT_DAYS_FILTER)).date()
            end_date_top_performers = current_date.date()

            top_player_df = calculate_player_scores(data, start_date=start_date_top_performers, end_date=end_date_top_performers).head(1)
            top_player_name = top_player_df.index[0]
            top_player_score = top_player_df[Constants.SCORE_COL].iloc[0]

            top_keeper_df = calculate_save_percentage(data, start_date=start_date_top_performers, end_date=end_date_top_performers).head(1)
            top_keeper_name = top_keeper_df.index[0]
            top_keeper_save_percentage = top_keeper_df[Constants.SAVE_PERCENTAGE_COL].iloc[0]

            performer_col1, performer_col2 = st.columns(2)
            with performer_col1:
                with st.expander("🏆 Top Player", expanded=False):
                    st.metric(
                        label="Score",
                        value=top_player_name,
                        delta=f"{top_player_score} points",
                        help=f"The player's score is calculated based on the outcome of their shots (goal: {Constants.GOAL_SCORE:.1f}, saved: {Constants.SAVED_SCORE:.1f}, out: {Constants.OUT_SCORE:.1f})."
                    )
            with performer_col2:
                with st.expander("🧤 Top Goalkeeper", expanded=False):
                    st.metric(
                        label="Save Percentage",
                        value=top_keeper_name,
                        delta=f"{top_keeper_save_percentage:.1f}% saves",
                        help="The percentage of penalties faced by the goalkeeper that were saved."
                    )
        
        with st.container(border=True):
            st.subheader("Recent Activity")
            st.markdown("Here's a summary of the latest penalty session. You can see the performance of each player and goalkeeper from the most recent game.")
            latest_date = data[Constants.DATE_COL].max()
            st.write(f"Latest session date: {latest_date}")

            latest_session_data = data[data[Constants.DATE_COL] == latest_date]

            player_stats = latest_session_data.groupby([Constants.SHOOTER_NAME_COL, Constants.STATUS_COL]).size().unstack(fill_value=0)
            st.write("Player Stats")
            st.dataframe(player_stats, use_container_width=True)

            keeper_stats = latest_session_data.groupby([Constants.KEEPER_NAME_COL, Constants.STATUS_COL]).size().unstack(fill_value=0)
            st.write("Keeper Stats")
            st.dataframe(keeper_stats, use_container_width=True)