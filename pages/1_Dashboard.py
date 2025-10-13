import time

import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_extras.skeleton import skeleton

from src import ui
from src import records
from src.constants import Columns, Data, Scoring, Status, UI
from src.analysis import calculate_keeper_scores, calculate_player_scores

if "reveal_player" not in st.session_state:
    st.session_state.reveal_player = False
if "reveal_keeper" not in st.session_state:
    st.session_state.reveal_keeper = False
if "reveal_top10_players" not in st.session_state:
    st.session_state.reveal_top10_players = False

ui.setup_page(
    page_title="Dashboard",
    page_icon="📊",
    page_description="""
    This dashboard shows an overview of penalty shootout data. You can explore player and goalkeeper stats and see historical trends.
    """,
    render_logo=True,
)


# --- Sidebar for Gender Selection ---
data = ui.load_and_process_data()

# --- Main Content ---
with st.container(border=True):
    st.subheader("Top Performers")
    st.markdown(
        f"This section shows the top players and goalkeepers from the last {UI.RECENT_DAYS_FILTER} days. Rankings use a time-weighted score, meaning recent games have a bigger impact."
    )
    st.page_link(
        "pages/3_Scoring_Method.py", label="ℹ️ Learn more about our scoring system"
    )

    current_date = pd.to_datetime(data[Columns.DATE]).max()
    start_date_top_performers = (
        current_date - pd.DateOffset(days=UI.RECENT_DAYS_FILTER)
    ).date()
    end_date_top_performers = current_date.date()

    top_player_df = calculate_player_scores(
        data, start_date=start_date_top_performers, end_date=end_date_top_performers
    ).head(1)
    top_player_name = top_player_df.index[0]
    top_player_score = top_player_df[Columns.SCORE].iloc[0]

    top_keeper_df = calculate_keeper_scores(
        data, start_date=start_date_top_performers, end_date=end_date_top_performers
    ).head(1)
    top_keeper_name = top_keeper_df.index[0]
    top_keeper_score = top_keeper_df[Columns.SCORE].iloc[0]

    top10_players_tab, player_tab, keeper_tab = st.tabs(
        [
            "🔟 Top-10 Players",
            "🏆 Top Player",
            "🧤 Top Goalkeeper",
        ]
    )

    with top10_players_tab:
        top10_players_button_placeholder = st.empty()
        if not st.session_state.reveal_top10_players:
            if top10_players_button_placeholder.button(
                "Reveal Top-10 Players", key="btn_reveal_top10_players"
            ):
                st.session_state.reveal_top10_players = True
                top10_players_button_placeholder.empty()  # Clear the button immediately
                countdown_placeholder = st.empty()
                for i in range(3, 0, -1):
                    countdown_placeholder.metric(
                        label="Revealing in...", value=f"{i} seconds"
                    )
                    time.sleep(1)
                countdown_placeholder.empty()  # Clear the countdown

        if st.session_state.reveal_top10_players:
            top_10_players_df = calculate_player_scores(
                data,
                start_date=start_date_top_performers,
                end_date=end_date_top_performers,
            ).head(10)

            if not top_10_players_df.empty:
                col_left, col_right = st.columns(2)
                players_list = list(top_10_players_df.itertuples(index=True, name=None))
                middle_index = round(len(players_list) / 2)

                col_left_items = []
                col_right_items = []

                for i, (name, score, goals, saved, out) in enumerate(players_list):
                    rank = i + 1
                    formatted_string = f"{rank:>2}. {name} `({score:.{Data.SCORE_DECIMAL_PLACES}f} pts)`\n"
                    if i < middle_index:
                        col_left_items.append(formatted_string)
                    else:
                        col_right_items.append(formatted_string)

                with col_left:
                    st.write_stream(ui.stream_data(col_left_items))

                with col_right:
                    st.write_stream(ui.stream_data(col_right_items))
            else:
                st.info("No top 10 players to display for the selected period.")

    with player_tab:
        player_button_placeholder = st.empty()
        if not st.session_state.reveal_player:
            if player_button_placeholder.button(
                "Reveal Top Player", key="btn_reveal_player"
            ):
                st.session_state.reveal_player = True
                player_button_placeholder.empty()  # Clear the button immediately
                countdown_placeholder = st.empty()
                for i in range(3, 0, -1):
                    countdown_placeholder.metric(
                        label="Revealing in...", value=f"{i} seconds"
                    )
                    time.sleep(1)
                countdown_placeholder.empty()  # Clear the countdown

        if st.session_state.reveal_player:
            st.metric(
                label="Score",
                value=top_player_name,
                delta=f"{top_player_score:.{Data.SCORE_DECIMAL_PLACES}f} points",
                help=f"The player's score is calculated based on the outcome of their shots (goal: {Scoring.GOAL:.1f}, saved: {Scoring.SAVED:.1f}, out: {Scoring.OUT:.1f}).",
            )

    with keeper_tab:
        keeper_button_placeholder = st.empty()
        if not st.session_state.reveal_keeper:
            if keeper_button_placeholder.button(
                "Reveal Top Goalkeeper", key="btn_reveal_keeper"
            ):
                st.session_state.reveal_keeper = True
                keeper_button_placeholder.empty()  # Clear the button immediately
                countdown_placeholder = st.empty()
                for i in range(3, 0, -1):
                    countdown_placeholder.metric(
                        label="Revealing in...", value=f"{i} seconds"
                    )
                    time.sleep(1)
                countdown_placeholder.empty()  # Clear the countdown

        if st.session_state.reveal_keeper:
            st.metric(
                label="Score",
                value=top_keeper_name,
                delta=f"{top_keeper_score:.{Data.SCORE_DECIMAL_PLACES}f} points",
                help=f"The goalkeeper's score is calculated based on the outcome of the shots they faced (goal: {Scoring.KEEPER_GOAL:.1f}, saved: {Scoring.KEEPER_SAVED:.1f}, out: {Scoring.KEEPER_OUT:.1f}).",
            )

with st.container(border=True):
    st.subheader("Hall of Fame")
    st.markdown(
        "See cool achievements, records, and fun facts about the penalty shootouts."
    )

    # Get records data
    longest_streak_players, longest_streak = records.get_longest_goal_streak(data)
    most_goals_player, most_goals_date, most_goals = records.get_most_goals_in_session(
        data
    )
    most_saves_keeper, most_saves_date, most_saves = records.get_most_saves_in_session(
        data
    )
    marathon_men, sessions = records.get_marathon_man(data)
    mysterious_ninjas, least_sessions = records.get_mysterious_ninja(data)
    busiest_date, busiest_count = records.get_busiest_day(data)
    rival_shooter, rival_keeper, encounters = records.get_biggest_rivalry(data)

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "🗓️ Current Year Records",
            "📅 Single Session Records",
            "🏆 All-Time Records",
            "✨ Fun Facts",
        ]
    )

    with tab1:
        current_year = pd.Timestamp.now().year
        current_year_data = data[
            pd.to_datetime(data[Columns.DATE]).dt.year == current_year
        ]

        col1_tab4, col2_tab4 = st.columns(2)

        with col1_tab4:
            if not current_year_data.empty:
                top_player_current_year_df = calculate_player_scores(
                    current_year_data
                ).head(1)
                if not top_player_current_year_df.empty:
                    top_player_current_year_name = top_player_current_year_df.index[0]
                    top_player_current_year_score = top_player_current_year_df[
                        Columns.SCORE
                    ].iloc[0]
                    st.metric(
                        label="⚽ Top Scorer",
                        value=top_player_current_year_name,
                        delta=f"{top_player_current_year_score:.{Data.SCORE_DECIMAL_PLACES}f} points",
                    )
                else:
                    skeleton(height=80)
            else:
                skeleton(height=80)

        with col2_tab4:
            if not current_year_data.empty:
                top_keeper_current_year_df = calculate_keeper_scores(
                    current_year_data
                ).head(1)
                if not top_keeper_current_year_df.empty:
                    top_keeper_current_year_name = top_keeper_current_year_df.index[0]
                    top_keeper_current_year_score = top_keeper_current_year_df[
                        Columns.SCORE
                    ].iloc[0]
                    st.metric(
                        label="🧤 Top Goalkeeper",
                        value=top_keeper_current_year_name,
                        delta=f"{top_keeper_current_year_score:.{Data.SCORE_DECIMAL_PLACES}f} points",
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
                help="Most goals scored by a player in a single game.",
            )
        with col2_tab2:
            st.metric(
                label="🧤 Most Saves in a Session",
                value=most_saves_keeper,
                delta=f"{most_saves} saves on {most_saves_date.strftime('%d-%m-%Y')}",
                help="Most saves made by a goalkeeper in a single game.",
            )

    with tab3:
        col1_tab1, col2_tab1 = st.columns(2)
        with col1_tab1:
            if not longest_streak_players:
                display_name = "N/A"
                help_text = "No goal streaks have been recorded yet."
            else:
                num_players = len(longest_streak_players)
                if num_players > UI.MAX_NAMES_IN_METRIC_DISPLAY:
                    display_name = f"{num_players} Players"
                    help_text = f"Players sharing the record: {', '.join(longest_streak_players)}"
                else:
                    display_name = ", ".join(longest_streak_players)
                    help_text = "Player(s) who scored the most goals in a row."

            st.metric(
                label="🏆 Longest Goal Streak",
                value=display_name,
                delta=f"{longest_streak} goal{'s' if longest_streak > 1 else ''}",
                help=help_text,
            )
        with col2_tab1:
            st.metric(
                label="⚔️ Biggest Rivalry",
                value=f"{rival_shooter} vs {rival_keeper}",
                delta=f"{encounters} encounters",
                help="The shooter and goalkeeper who played against each other the most.",
            )

    with tab4:
        col1_tab3, col2_tab3 = st.columns(2)
        with col1_tab3:
            if not marathon_men:
                display_name = "N/A"
                help_text = "No session data available."
            else:
                num_players = len(marathon_men)
                if num_players > UI.MAX_NAMES_IN_METRIC_DISPLAY:
                    display_name = f"{', '.join(marathon_men[:UI.MAX_NAMES_IN_METRIC_DISPLAY])}, +{num_players - UI.MAX_NAMES_IN_METRIC_DISPLAY} people"
                    help_text = (
                        f"Players with the most sessions: {', '.join(marathon_men)}"
                    )
                else:
                    display_name = ", ".join(marathon_men)
                    help_text = "Player(s) who played in the most games."

            st.metric(
                label="🏃 Marathon Man (Most Sessions)",
                value=display_name,
                delta=f"{sessions} session{'s' if sessions > 1 else ''}",
                help=help_text,
            )
        with col2_tab3:
            if not mysterious_ninjas:
                display_name = "N/A"
                help_text = "No session data available."
            else:
                num_players = len(mysterious_ninjas)
                if num_players > UI.MAX_NAMES_IN_METRIC_DISPLAY:
                    display_name = f"{', '.join(mysterious_ninjas[:UI.MAX_NAMES_IN_METRIC_DISPLAY])}, +{num_players - UI.MAX_NAMES_IN_METRIC_DISPLAY} people"
                    help_text = f"Players with the fewest sessions: {', '.join(mysterious_ninjas)}"
                else:
                    display_name = ", ".join(mysterious_ninjas)
                    help_text = "Player(s) who played in the fewest games."

            st.metric(
                label="🥷 Mysterious Ninja (Fewest Sessions)",
                value=display_name,
                delta=f"{least_sessions} session{'s' if least_sessions > 1 else ''}",
                help=help_text,
            )

        col1_tab4, col2_tab4 = st.columns(2)
        with col1_tab4:
            st.metric(
                label="🗓️ Busiest Day",
                value=busiest_date.strftime("%d %B, %Y"),
                delta=f"{busiest_count} penalties",
                help="The date with the most penalties.",
            )


# Recent Activity content (full width)
with st.container(border=True):
    st.subheader("Recent Activity")
    st.markdown(
        "A summary of the last game, including player and goalkeeper performance. You can compare the latest stats with the game before."
    )

    # Get unique sorted dates
    unique_dates = sorted(data[Columns.DATE].unique(), reverse=True)

    latest_date = unique_dates[0]
    formatted_latest_date = latest_date.strftime("%d %B, %Y")
    st.markdown(f"Latest session date: `{formatted_latest_date}`")

    latest_session_data = data[data[Columns.DATE] == latest_date]

    # Calculate aggregated metrics for the latest session
    total_goals_latest = len(
        latest_session_data[latest_session_data[Columns.STATUS] == Status.GOAL]
    )
    total_saves_latest = len(
        latest_session_data[latest_session_data[Columns.STATUS] == Status.SAVED]
    )
    total_outs_latest = len(
        latest_session_data[latest_session_data[Columns.STATUS] == Status.OUT]
    )

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
        previous_session_data = data[data[Columns.DATE] == previous_date]

        total_goals_previous = len(
            previous_session_data[previous_session_data[Columns.STATUS] == Status.GOAL]
        )
        total_saves_previous = len(
            previous_session_data[previous_session_data[Columns.STATUS] == Status.SAVED]
        )
        total_outs_previous = len(
            previous_session_data[previous_session_data[Columns.STATUS] == Status.OUT]
        )

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
            help="Goals in the last game. The change from the game before is also shown.",
        )
    with col_metrics2:
        st.metric(
            label="Saves",
            value=total_saves_latest,
            delta=delta_saves,
            help="Saves in the last game. The change from the game before is also shown.",
        )
    with col_metrics3:
        st.metric(
            label="Outs",
            value=total_outs_latest,
            delta=delta_outs,
            delta_color="inverse",
            help="Shots that went out in the last game. The change from the game before is also shown.",
        )

    # Use tabs for Player and Keeper Stats
    tab_players, tab_keepers = st.tabs(["Player Stats", "Keeper Stats"])

    with tab_players:
        player_stats = (
            latest_session_data.groupby([Columns.SHOOTER_NAME, Columns.STATUS])
            .size()
            .unstack(fill_value=0)
        )
        player_scores = calculate_player_scores(latest_session_data)
        player_stats = player_stats.join(player_scores[Columns.SCORE])
        player_stats = player_stats.sort_values(by=Columns.SCORE, ascending=False)
        fig = px.bar(player_stats, x=player_stats.index, y=Columns.SCORE)
        ui.configure_plotly_layout(fig, player_stats[Columns.SCORE])
        ui.render_plotly_chart(fig, fixed_range=True)
        st.dataframe(player_stats, width="stretch")

    with tab_keepers:
        keeper_stats = (
            latest_session_data.groupby([Columns.KEEPER_NAME, Columns.STATUS])
            .size()
            .unstack(fill_value=0)
        )
        keeper_scores = calculate_keeper_scores(latest_session_data)
        keeper_stats = keeper_stats.join(keeper_scores[Columns.SCORE])
        keeper_stats = keeper_stats.sort_values(by=Columns.SCORE, ascending=False)
        fig = px.bar(keeper_stats, x=keeper_stats.index, y=Columns.SCORE)
        ui.configure_plotly_layout(fig, keeper_stats[Columns.SCORE])
        ui.render_plotly_chart(fig, fixed_range=True)
        st.dataframe(keeper_stats, width="stretch")