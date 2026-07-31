import os
import requests
import pandas as pd


def create_game_result_csv(year):

    base_folder = os.path.join(
        "game_results",
        str(year)
    )

    os.makedirs(
        base_folder,
        exist_ok=True
    )

    url = (
        "https://site.api.espn.com/apis/site/v2/sports/"
        "football/nfl/scoreboard"
    )

    team_results = {}


    for week in range(1, 19):

        params = {
            "dates": year,
            "week": week
        }

        response = requests.get(
            url,
            params=params
        )

        data = response.json()


        for game in data["events"]:

            competition = game["competitions"][0]

            teams = competition["competitors"]

            home = None
            away = None


            for team in teams:

                if team["homeAway"] == "home":
                    home = team
                else:
                    away = team


            home_abbr = home["team"]["abbreviation"]
            away_abbr = away["team"]["abbreviation"]


            home_score = int(home["score"])
            away_score = int(away["score"])


            if home_score > away_score:
                winner = home_abbr
            else:
                winner = away_abbr


            # Home team result
            if home_abbr not in team_results:
                team_results[home_abbr] = []

            team_results[home_abbr].append(
                {
                    "week": week,
                    "opponent": away_abbr,
                    "result": (
                        "WIN"
                        if winner == home_abbr
                        else "LOSS"
                    )
                }
            )


            # Away team result
            if away_abbr not in team_results:
                team_results[away_abbr] = []

            team_results[away_abbr].append(
                {
                    "week": week,
                    "opponent": home_abbr,
                    "result": (
                        "WIN"
                        if winner == away_abbr
                        else "LOSS"
                    )
                }
            )


    # Write CSVs
    for team, games in team_results.items():

        team_folder = os.path.join(
            base_folder,
            team
        )

        os.makedirs(
            team_folder,
            exist_ok=True
        )


        df = pd.DataFrame(games)


        df.to_csv(
            os.path.join(
                team_folder,
                "results.csv"
            ),
            index=False
        )


if __name__ == "__main__":

    for year in range(2024, 2026):
        create_game_result_csv(year)