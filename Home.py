import pandas as pd
import streamlit as st
import plotly.express as px
import time
from streamlit_extras.skeleton import skeleton


from utils import (
    load_data, calculate_player_scores, 
    calculate_save_percentage, Constants, get_recent_penalties,
    get_longest_goal_streak, get_most_goals_in_session,
    get_most_saves_in_session, get_marathon_man, get_busiest_day, 
    get_biggest_rivalry
)

if "reveal_player" not in st.session_state:
    st.session_state.reveal_player = False
if "reveal_keeper" not in st.session_state:
    st.session_state.reveal_keeper = False

st.set_page_config(
    page_title="NFT Weingarten - Penalty Tracker",
    page_icon=Constants.EMOJI_HOME_PAGE,
    initial_sidebar_state="expanded",
    layout="wide"
)

# --- Header ---

col1, col2, col3 = st.columns([1,0.5,1])
with col2:
    st.image(Constants.LOGO_PATH, use_container_width=True)

st.markdown("<h1 style='text-align: center;'>NFT Weingarten Penalty Tracker</h1>", unsafe_allow_html=True)

st.markdown(
    """
    Welcome to the **NFT Weingarten Penalty Tracker**! This interactive dashboard provides a comprehensive overview of penalty shootout data. Explore player performances, goalkeeper statistics, and historical trends to gain insights into the game.
    """
)
st.write("")

st.markdown("---")

# --- Load Data ---
data = load_data()
if not data.empty:
    data[Constants.DATE_COL] = pd.to_datetime(data[Constants.DATE_COL]).dt.date

    # --- Main Content ---
    col_hof, col_top_performers = st.columns(2, gap="large")

    with col_hof:


        with st.container(border=True):
            st.subheader("Hall of Fame")
            st.markdown("Discover the most remarkable achievements and milestones in our penalty shootout history. Explore all-time records, single-session heroics, and fun facts across various categories.")
            
            # Get records data
            longest_streak_player, longest_streak = get_longest_goal_streak(data)
            most_goals_player, most_goals_date, most_goals = get_most_goals_in_session(data)
            most_saves_keeper, most_saves_date, most_saves = get_most_saves_in_session(data)
            marathon_man, sessions = get_marathon_man(data)
            busiest_date, busiest_count = get_busiest_day(data)
            rival_shooter, rival_keeper, encounters = get_biggest_rivalry(data)

            tab1, tab2, tab3, tab4 = st.tabs(["🗓️ Current Year Records", "📅 Single Session Records", "🏆 All-Time Records", "✨ Fun Facts"])

            with tab1:
                current_year = pd.Timestamp.now().year
                current_year_data = data[pd.to_datetime(data[Constants.DATE_COL]).dt.year == current_year]

                col1_tab4, col2_tab4 = st.columns(2)

                with col1_tab4:
                    if not current_year_data.empty:
                        top_player_current_year_df = calculate_player_scores(current_year_data).head(1)
                        if not top_player_current_year_df.empty:
                            top_player_current_year_name = top_player_current_year_df.index[0]
                            top_player_current_year_score = top_player_current_year_df[Constants.SCORE_COL].iloc[0]
                            st.metric(
                                label="⚽ Top Scorer",
                                value=top_player_current_year_name,
                                delta=f"{top_player_current_year_score} points"
                            )
                        else:
                            skeleton(height=80)
                    else:
                        skeleton(height=80)

                with col2_tab4:
                    if not current_year_data.empty:
                        top_keeper_current_year_df = calculate_save_percentage(current_year_data).head(1)
                        if not top_keeper_current_year_df.empty:
                            top_keeper_current_year_name = top_keeper_current_year_df.index[0]
                            top_keeper_current_year_save_percentage = top_keeper_current_year_df[Constants.SAVE_PERCENTAGE_COL].iloc[0]
                            st.metric(
                                label="🧤 Top Goalkeeper",
                                value=top_keeper_current_year_name,
                                delta=f"{top_keeper_current_year_save_percentage:.1f}% saves"
                            )
                        else:
                            skeleton(height=80)
                    else:
                        skeleton(height=80)

            with tab2:
                col1_tab2, col2_tab2 = st.columns(2)
                with col1_tab2:
                    st.metric(
                        label="⚽ Most Goals in a Session",
                        value=most_goals_player,
                        delta=f"{most_goals} goals on {most_goals_date.strftime('%d-%m-%Y')}",
                        help="The player who scored the most goals in a single session."
                    )
                with col2_tab2:
                    st.metric(
                        label="🧤 Most Saves in a Session",
                        value=most_saves_keeper,
                        delta=f"{most_saves} saves on {most_saves_date.strftime('%d-%m-%Y')}",
                        help="The goalkeeper who made the most saves in a single session."
                    )

            with tab3:
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

            with tab4:
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
                        value=busiest_date.strftime("%d %B, %Y"),
                        delta=f"{busiest_count} penalties",
                        help="The date with the highest number of penalties taken."
                    )

    with col_top_performers:
        with st.container(border=True):
            st.subheader("Top Performers")
            st.markdown(f"Highlights top-performing players and goalkeepers from the `recent {Constants.RECENT_DAYS_FILTER} days`, showcasing their current form and impact.")
            
            current_date = pd.to_datetime(data[Constants.DATE_COL]).max()
            start_date_top_performers = (current_date - pd.DateOffset(days=Constants.RECENT_DAYS_FILTER)).date()
            end_date_top_performers = current_date.date()

            top_player_df = calculate_player_scores(data, start_date=start_date_top_performers, end_date=end_date_top_performers).head(1)
            top_player_name = top_player_df.index[0]
            top_player_score = top_player_df[Constants.SCORE_COL].iloc[0]

            top_keeper_df = calculate_save_percentage(data, start_date=start_date_top_performers, end_date=end_date_top_performers).head(1)
            top_keeper_name = top_keeper_df.index[0]
            top_keeper_save_percentage = top_keeper_df[Constants.SAVE_PERCENTAGE_COL].iloc[0]

            player_tab, keeper_tab = st.tabs(["🏆 Top Player", "🧤 Top Goalkeeper"])

            with player_tab:
                player_button_placeholder = st.empty()
                if not st.session_state.reveal_player:
                    if player_button_placeholder.button("Reveal Top Player", key="btn_reveal_player"):
                        st.session_state.reveal_player = True
                        player_button_placeholder.empty() # Clear the button immediately
                        countdown_placeholder = st.empty()
                        for i in range(3, 0, -1):
                            countdown_placeholder.metric(label="Revealing in...", value=f"{i} seconds")
                            time.sleep(1)
                        countdown_placeholder.empty() # Clear the countdown

                if st.session_state.reveal_player:
                    st.metric(
                        label="Score",
                        value=top_player_name,
                        delta=f"{top_player_score} points",
                        help=f"The player\'s score is calculated based on the outcome of their shots (goal: {Constants.GOAL_SCORE:.1f}, saved: {Constants.SAVED_SCORE:.1f}, out: {Constants.OUT_SCORE:.1f})."
                    )

            with keeper_tab:
                keeper_button_placeholder = st.empty()
                if not st.session_state.reveal_keeper:
                    if keeper_button_placeholder.button("Reveal Top Goalkeeper", key="btn_reveal_keeper"):
                        st.session_state.reveal_keeper = True
                        keeper_button_placeholder.empty() # Clear the button immediately
                        countdown_placeholder = st.empty()
                        for i in range(3, 0, -1):
                            countdown_placeholder.metric(label="Revealing in...", value=f"{i} seconds")
                            time.sleep(1)
                        countdown_placeholder.empty() # Clear the countdown

                if st.session_state.reveal_keeper:
                    st.metric(
                        label="Save Percentage",
                        value=top_keeper_name,
                        delta=f"{top_keeper_save_percentage:.1f}% saves",
                        help="The percentage of penalties faced by the goalkeeper that were saved."
                    )

    # Recent Activity content (full width)
    with st.container(border=True):
        st.subheader("Recent Activity")
        st.markdown("A summary of the latest penalty session, including player and goalkeeper performance. Compare current stats with the previous session for quick insights.")

        # Get unique sorted dates
        unique_dates = sorted(data[Constants.DATE_COL].unique(), reverse=True)

        latest_date = unique_dates[0]
        formatted_latest_date = latest_date.strftime("%d %B, %Y")
        st.markdown(f"Latest session date: <span style='color: green;'>{formatted_latest_date}</span>", unsafe_allow_html=True)

        latest_session_data = data[data[Constants.DATE_COL] == latest_date]

        # Calculate aggregated metrics for the latest session
        total_goals_latest = len(latest_session_data[latest_session_data[Constants.STATUS_COL] == Constants.GOAL_STATUS])
        total_saves_latest = len(latest_session_data[latest_session_data[Constants.STATUS_COL] == Constants.SAVED_STATUS])
        total_outs_latest = len(latest_session_data[latest_session_data[Constants.STATUS_COL] == Constants.OUT_STATUS])

        # Initialize previous session metrics and deltas
        total_goals_previous = 0
        total_saves_previous = 0
        total_outs_previous = 0
        delta_goals = 0
        delta_saves = 0
        delta_outs = 0

        # Check if there's a previous session
        if len(unique_dates) > 1:
            previous_date = unique_dates[1]
            previous_session_data = data[data[Constants.DATE_COL] == previous_date]

            total_goals_previous = len(previous_session_data[previous_session_data[Constants.STATUS_COL] == Constants.GOAL_STATUS])
            total_saves_previous = len(previous_session_data[previous_session_data[Constants.STATUS_COL] == Constants.SAVED_STATUS])
            total_outs_previous = len(previous_session_data[previous_session_data[Constants.STATUS_COL] == Constants.OUT_STATUS])

            delta_goals = total_goals_latest - total_goals_previous
            delta_saves = total_saves_latest - total_saves_previous
            delta_outs = total_outs_latest - total_outs_previous

        # Display aggregated metrics with deltas
        _, col_metrics1, _, col_metrics2, _, col_metrics3, _ = st.columns(7)
        with col_metrics1:
            st.metric(
                label="Goals",
                value=total_goals_latest,
                delta=delta_goals,
                help="Latest session's goals. Delta: change from previous session."
            )
        with col_metrics2:
            st.metric(
                label="Saves",
                value=total_saves_latest,
                delta=delta_saves,
                help="Latest session's saves. Delta: change from previous session."
            )
        with col_metrics3:
            st.metric(
                label="Outs",
                value=total_outs_latest,
                delta=delta_outs,
                help="Latest session's outs. Delta: change from previous session."
            )


        # Use tabs for Player and Keeper Stats
        tab_players, tab_keepers = st.tabs(["Player Stats", "Keeper Stats"])

        with tab_players:
            player_stats = latest_session_data.groupby([Constants.SHOOTER_NAME_COL, Constants.STATUS_COL]).size().unstack(fill_value=0)
            st.dataframe(player_stats, use_container_width=True)

        with tab_keepers:
            keeper_stats = latest_session_data.groupby([Constants.KEEPER_NAME_COL, Constants.STATUS_COL]).size().unstack(fill_value=0)
            st.dataframe(keeper_stats, use_container_width=True)