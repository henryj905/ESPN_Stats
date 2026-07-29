import pandas as pd

import Schedule
from Schedule import get_week_data, get_game_summary
from stat_aggregation import aggregate_stats
import os


def get_stat_category(year, week, category_name):

    player_stats = []

    games = get_week_data(year, week)

    for game in games["events"]:

        game_id = game["id"]

        summary = get_game_summary(game_id)

        for team in summary["boxscore"]["players"]:

            team_abbr = team["team"]["abbreviation"]

            for category in team["statistics"]:

                if category["name"] != category_name:
                    continue

                for athlete in category["athletes"]:

                    row = {
                        "team": team_abbr,
                        "player": athlete["athlete"]["displayName"],
                        "category": category_name
                    }

                    # Add stats as columns
                    for label, value in zip(category["labels"], athlete["stats"]):
                        row[label] = value

                    player_stats.append(row)

    df = pd.DataFrame(player_stats)

    if df.empty:
        return df

    return df.sort_values("team").reset_index(drop=True)


def get_passing(year, week):
    return get_stat_category(year, week, "passing")


def get_rushing(year, week):
    return get_stat_category(year, week, "rushing")


def get_receiving(year, week):
    return get_stat_category(year, week, "receiving")


def get_fumbles(year, week):
    return get_stat_category(year, week, "fumbles")


def get_defensive(year, week):
    return get_stat_category(year, week, "defensive")


def get_kicking(year, week):
    return get_stat_category(year, week, "kicking")


def get_punting(year, week):
    return get_stat_category(year, week, "punting")


def get_interceptions(year, week):
    return get_stat_category(year, week, "interceptions")


def get_kick_returns(year, week):
    return get_stat_category(year, week, "kick_returns")


def save_player_stats_cache(year, week, stat_dfs):

    # Main cache folder
    main_folder = "player_stats_cache"

    if not os.path.exists(main_folder):
        os.makedirs(main_folder)


    # Year folder
    year_folder = os.path.join(
        main_folder,
        f"player_stats_cache_{year}"
    )

    if not os.path.exists(year_folder):
        os.makedirs(year_folder)


    # Week folder
    week_folder = os.path.join(
        year_folder,
        f"player_stats_cache_{year}_{week}"
    )

    if not os.path.exists(week_folder):
        os.makedirs(week_folder)

    # Save each category
    for category, df in stat_dfs.items():

        # Skip empty DataFrames
        if df.empty:
            continue

        file_path = os.path.join(
            week_folder,
            f"{category}.csv"
        )

        df.to_csv(
            file_path,
            index=False
        )

    print(f"Saved cache: {year} Week {week}")


def cache_exists(year, week):

    path = os.path.join(
        "player_stats_cache",
        f"player_stats_cache_{year}",
        f"player_stats_cache_{year}_{week}"
    )

    return os.path.exists(path)


def get_season_stats(year, team_abbr):

    year_folder = os.path.join(
        "player_stats_cache",
        f"player_stats_cache_{year}"
    )

    if not os.path.exists(year_folder):
        return {}

    season_categories = {}

    for week_folder in sorted(os.listdir(year_folder)):

        week_path = os.path.join(year_folder, week_folder)

        if not os.path.isdir(week_path):
            continue

        for file in os.listdir(week_path):

            if not file.endswith(".csv"):
                continue

            category = file[:-4]

            path = os.path.join(week_path, file)

            try:
                df = pd.read_csv(path)
            except pd.errors.EmptyDataError:
                continue

            if "team" not in df.columns:
                continue

            df = df[df["team"] == team_abbr]

            if df.empty:
                continue

            if category not in season_categories:
                season_categories[category] = []

            season_categories[category].append(df)

    season_stats = {}

    for category, dfs in season_categories.items():
        combined = pd.concat(
            dfs,
            ignore_index=True
        )

        # Split C/ATT into completions and attempts
        if "C/ATT" in combined.columns:
            split_values = combined["C/ATT"].str.split("/", expand=True)

            combined["COMP"] = pd.to_numeric(
                split_values[0],
                errors="coerce"
            )

            combined["ATT"] = pd.to_numeric(
                split_values[1],
                errors="coerce"
            )

            combined = combined.drop(columns=["C/ATT"])

        # Split FG into field goals made and attempts
        if "FG" in combined.columns:
            split_values = combined["FG"].str.split("/", expand=True)

            combined["FG_MADE"] = pd.to_numeric(
                split_values[0],
                errors="coerce"
            )

            combined["FG_ATT"] = pd.to_numeric(
                split_values[1],
                errors="coerce"
            )

            combined = combined.drop(columns=["FG"])


        # Split XP into extra points made and attempts
        if "XP" in combined.columns:
            split_values = combined["XP"].str.split("/", expand=True)

            combined["EX_MADE"] = pd.to_numeric(
                split_values[0],
                errors="coerce"
            )

            combined["EX_ATT"] = pd.to_numeric(
                split_values[1],
                errors="coerce"
            )

            combined = combined.drop(columns=["XP"])

        combined = aggregate_stats(
            combined,
            category,
            ["team", "player", "category"]
        )

        combined = combined.sort_values(
            ["team", "player"]
        ).reset_index(drop=True)

        season_stats[category] = combined
    return season_stats


def save_season_stats(year, team, season_stats):

    # Create year folder
    year_folder = os.path.join(
        "player_stats_season",
        f"player_stats_season_{year}"
    )

    # Create team folder
    team_folder = os.path.join(
        year_folder,
        f"player_stats_season_{team}"
    )

    os.makedirs(
        team_folder,
        exist_ok=True
    )

    # Save each category
    for category, df in season_stats.items():

        filename = f"player_stats_season_{category}.csv"

        filepath = os.path.join(
            team_folder,
            filename
        )

        df.to_csv(
            filepath,
            index=False
        )

        print(f"Saved {category} -> {filepath}")


if __name__ == "__main__":
    # for year in [2024, 2025]:
    #
    #     for week in range(1, 19):  # NFL regular season weeks
    #
    #         if cache_exists(year, week):
    #             print(f"{year} Week {week} already cached")
    #             continue
    #
    #         print(f"Gathering {year} Week {week}")
    #
    #         stats = {
    #             "passing": get_passing(year, week),
    #             "rushing": get_rushing(year, week),
    #             "receiving": get_receiving(year, week),
    #             "fumbles": get_fumbles(year, week),
    #             "defensive": get_defensive(year, week),
    #             "interceptions": get_interceptions(year, week),
    #             "kickReturns": get_kick_returns(year, week),
    #             "kicking": get_kicking(year, week),
    #             "punting": get_punting(year, week)
    #         }
    #
    #         save_player_stats_cache(year, week, stats)
    # get = ''
    # for year in range(2024, 2027):
    #     for team in Schedule.getonlyabbreviations(2025):
    for year in range(2024, 2026):
        for team in Schedule.getonlyabbreviations(year):
            season = get_season_stats(year, team)
            save_season_stats(year, team, season)