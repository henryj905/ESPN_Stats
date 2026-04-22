import requests
import pandas as pd


def get_week_data(week):
    url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    return requests.get(url, params={"seasontype": 2, "week": week}).json()


def get_game_summary(game_id):
    url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={game_id}"
    return requests.get(url).json()


def extract_player_stats(game_id):
    game = get_game_summary(game_id)

    rows = []

    if "boxscore" not in game:
        return rows

    for team in game["boxscore"]["players"]:
        team_name = team["team"]["displayName"]

        for stat_group in team.get("statistics", []):

            stat_type = stat_group.get("name")  # 👈 THIS is the key fix

            for athlete in stat_group.get("athletes", []):

                player = athlete.get("athlete", {})
                stats = athlete.get("stats", [])
                labels = stat_group.get("labels", [])

                row = {
                    "game_id": game_id,
                    "team": team_name,
                    "player": player.get("displayName"),
                    "position": player.get("position", {}).get("abbreviation"),
                    "stat_type": stat_type   # 👈 ADD THIS
                }

                for i, value in enumerate(stats):
                    if i < len(labels):
                        row[labels[i]] = value

                rows.append(row)

    return rows


def build_week_dataframe(week):
    week_data = get_week_data(week)

    all_rows = []

    for event in week_data["events"]:
        game_id = event["id"]
        all_rows.extend(extract_player_stats(game_id))

    return pd.DataFrame(all_rows)


def create_df():
    df = build_week_dataframe(1)

    df_pivot = df.pivot_table(
        index=["game_id", "player", "team"],
        columns="stat_type",
        aggfunc="first"
    )

    df_pivot.columns = [
        f"{stat}_{col}" for col, stat in df_pivot.columns
    ]

    df_pivot = df_pivot.reset_index()

    df_pivot = df_pivot.dropna(how="all")
    df_pivot = df_pivot.dropna(axis=1, how="all")

    keep_cols = [col for col in df_pivot.columns if any(x in col for x in ["passing", "rushing", "receiving"])
                 or col in ["game_id", "player", "team"]]

    df_pivot = df_pivot[keep_cols]

    pd.set_option("display.max_columns", None)
    print(df_pivot)
    df_pivot = df_pivot.sort_values(['team'])
    return df_pivot

