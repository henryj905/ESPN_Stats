import os
import pandas as pd

from stat_aggregation import aggregate_team_stats


def get_weekly_stats(year, week, team_abbr):

    week_folder = os.path.join(
        "player_stats_cache",
        f"player_stats_cache_{year}",
        f"player_stats_cache_{year}_{week}"
    )

    if not os.path.exists(week_folder):
        return {}

    weekly_stats = {}

    # Read each category CSV
    for file in os.listdir(week_folder):

        if not file.endswith(".csv"):
            continue

        category = file[:-4]

        path = os.path.join(
            week_folder,
            file
        )

        try:
            df = pd.read_csv(path)
        except pd.errors.EmptyDataError:
            continue

        # Skip files without a team column
        if "team" not in df.columns:
            continue

        # Keep only the requested team
        df = df[df["team"] == team_abbr]

        if df.empty:
            continue

        # Combine all player stats into one team row
        combined = aggregate_team_stats(
            df,
            category
        )

        # Add the category column back
        combined.insert(
            1,
            "category",
            category
        )

        weekly_stats[category] = combined

    return weekly_stats


# Use this for gathering previous weeks for comparison
def combine_weekly_stats(dfs):

    combined_categories = {}

    # Go through each week's stats
    for week in dfs:

        # Go through each category in that week
        for category, df in week.items():

            if category not in combined_categories:
                combined_categories[category] = []

            combined_categories[category].append(df)

    # Combine each category
    final_stats = {}

    for category, frames in combined_categories.items():

        combined = pd.concat(
            frames,
            ignore_index=True
        )

        final_stats[category] = aggregate_team_stats(
            combined,
            category
        )

        final_stats[category].insert(
            1,
            "category",
            category
        )

    return final_stats


# if __name__ == "__main__":
#     previous_weeks = []
#     for week in range(1, 19):
#         stats = get_weekly_stats(
#             2025,
#             week,
#             "DAL"
#         )
#         previous_weeks.append(stats)
#         # for category, df in stats.items():
#         #     print(df)
#     season = combine_weekly_stats(previous_weeks)
#
#     for category, df in season.items():
#         print(df)