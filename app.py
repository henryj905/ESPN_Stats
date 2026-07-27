import streamlit as st
import pandas as pd
import os
from Schedule import single_team_schedule, getonlyabbreviations
from player_stats import (
    get_passing,
    get_rushing,
    get_receiving,
    get_defensive,
    get_kicking,
    get_punting
)


# Title
st.title("NFL Predictor")


# Select mode
mode = st.selectbox(
    "Select Option",
    ["Schedule", "Stats"]
)


# ==========================
# SCHEDULE SECTION
# ==========================

if mode == "Schedule":

    st.write("Select a season and team to view their schedule")

    # Year selection
    year = st.selectbox(
        "Select Year",
        [2026, 2025, 2024, 2023, 2022]
    )

    # Get teams
    teams = getonlyabbreviations(year)

    # Remove duplicates
    teams = sorted(list(set(teams)))

    # Team selection
    team = st.selectbox(
        "Select Team",
        teams
    )

    # Button
    if st.button("View Schedule"):

        schedule = single_team_schedule(year, team)

        st.subheader(f"{team} Schedule ({year})")

        st.dataframe(
            schedule,
            use_container_width=True
        )


# ==========================
# STATS SECTION
# ==========================

elif mode == "Stats":

    st.write("Select what type of stats you want to view")

    stats_type = st.selectbox(
        "Stats Type",
        [
            "Weekly Stats",
            "Season Totals"
        ]
    )


    # ==========================
    # WEEKLY STATS
    # ==========================

    if stats_type == "Weekly Stats":

        st.write("Select a season, week, and category")

        year = st.selectbox(
            "Select Year",
            [2025, 2024]
        )

        week = st.selectbox(
            "Select Week",
            list(range(1, 19))
        )

        category = st.selectbox(
            "Select Category",
            [
                "Passing",
                "Rushing",
                "Receiving",
                "Defense",
                "Kicking",
                "Punting"
            ]
        )

        category_functions = {
            "Passing": get_passing,
            "Rushing": get_rushing,
            "Receiving": get_receiving,
            "Defense": get_defensive,
            "Kicking": get_kicking,
            "Punting": get_punting
        }


        if st.button("View Weekly Stats"):

            stats = category_functions[category](year, week)

            st.subheader(
                f"{year} Week {week} {category} Stats"
            )

            st.dataframe(
                stats,
                use_container_width=True
            )


    # ==========================
    # SEASON TOTALS
    # ==========================

    elif stats_type == "Season Totals":

        st.write("Select a season, team, and category")

        year = st.selectbox(
            "Select Season",
            [2025, 2024]
        )


        teams = getonlyabbreviations(year)
        teams = sorted(list(set(teams)))


        team = st.selectbox(
            "Select Team",
            teams
        )


        category = st.selectbox(
            "Select Category",
            [
                "passing",
                "rushing",
                "receiving",
                "defensive",
                "kicking",
                "punting"
            ]
        )


        if st.button("View Season Stats"):

            file_path = os.path.join(
                "player_stats_season",
                f"player_stats_season_{year}",
                f"player_stats_season_{team}",
                f"player_stats_season_{category}.csv"
            )


            if os.path.exists(file_path):

                season_stats = pd.read_csv(file_path)

                st.subheader(
                    f"{year} {team} Season {category.title()} Stats"
                )

                st.dataframe(
                    season_stats,
                    use_container_width=True
                )

            else:

                st.error(
                    f"No season stats found for {team} {year} {category}"
                )