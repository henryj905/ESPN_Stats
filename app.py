import streamlit as st

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

    st.write("Select a season, week, and category")

    # Year selection
    year = st.selectbox(
        "Select Year",
        [2025, 2024]
    )

    # Week selection
    week = st.selectbox(
        "Select Week",
        list(range(1, 19))
    )

    # Category selection
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

    # Map categories to functions
    category_functions = {
        "Passing": get_passing,
        "Rushing": get_rushing,
        "Receiving": get_receiving,
        "Defense": get_defensive,
        "Kicking": get_kicking,
        "Punting": get_punting
    }

    # Button
    if st.button("View Stats"):
        stats = category_functions[category](year, week)

        st.subheader(
            f"{year} Week {week} {category} Stats"
        )

        st.dataframe(
            stats,
            use_container_width=True
        )
