import streamlit as st
from Schedule import single_team_schedule, getonlyabbreviations


# Title
st.title("NFL Predictor")

st.write("Select a season and team to view their schedule")


# Year selection
year = st.selectbox(
    "Select Year",
    [2026, 2025, 2024, 2023, 2022]
)


# Get teams for selected year
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