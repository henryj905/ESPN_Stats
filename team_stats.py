import os
import pandas as pd

import Schedule
from stat_aggregation import aggregate_team_stats


def get_team_stats(year, team):

    team_folder = os.path.join(
        "player_stats_season",
        f"player_stats_season_{year}",
        f"player_stats_season_{team}"
    )

    if not os.path.exists(team_folder):
        return {}

    team_stats = {}

    for file in os.listdir(team_folder):

        if not file.endswith(".csv"):
            continue

        category = (
            file
            .replace("player_stats_season_", "")
            .replace(".csv", "")
        )

        path = os.path.join(
            team_folder,
            file
        )

        df = pd.read_csv(path)

        if "player" in df.columns:
            df = df.drop(columns=["player"])

        combined = aggregate_team_stats(
            df,
            category
        )

        combined.insert(
            1,
            "category",
            category
        )
        team_stats[category] = combined

    return team_stats


def save_team_stats(year, team, team_stats):
    year_folder = os.path.join(
        "team_stats_season",
        f"team_stats_season_{year}"
    )

    team_folder = os.path.join(
        year_folder,
        f"team_stats_season_{team}"
    )

    os.makedirs(
        team_folder,
        exist_ok=True
    )

    for category, df in team_stats.items():

        filename = f"team_stats_season_{category}.csv"

        filepath = os.path.join(
            team_folder,
            filename
        )

        df.to_csv(
            filepath,
            index=False
        )


if __name__ == "__main__":

    # stats = get_team_stats(
    #     2025,
    #     "DAL"
    # )
    #
    # save_team_stats(
    #     2025,
    #     "DAL",
    #     stats
    # )

    for year in range(2021, 2026):
        for team in Schedule.getonlyabbreviations(year):
            stats = get_team_stats(year, team)
            save_team_stats(year, team, stats)
