import requests
import pandas as pd
import os


def get_week_data(year, week):
    url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    return requests.get(url, params={"dates": year, "seasontype": 2, "week": week}).json()


def get_game_summary(game_id):
    url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={game_id}"
    return requests.get(url).json()


dataframe_cache = {}
# creates a dataframe with columns: game_id, home_team, away_team
# Input week returns matchups for given input


def gameidhomeaway(year, week):
    # If we already created this week, return the saved dataframe
    if (year, week) in dataframe_cache:
        return dataframe_cache[(year, week)]
    game_id_list = []
    home_list = []
    home_abbr_list = []
    away_list = []
    away_abbr_list = []

    all_game_data = get_week_data(year, week)

    for x in all_game_data['events']:
        game_id_list.append(x['id'])

        teams = x['name'].split(' at ')
        home_list.append(teams[1])
        away_list.append(teams[0])

        teams_abbr = x['shortName'].replace(' VS ', ' @ ').split(" @ ")
        home_abbr_list.append(teams_abbr[1])
        away_abbr_list.append(teams_abbr[0])

    d = {"game_id": game_id_list, "home_team": home_list, "home_abbr": home_abbr_list,
         "away_team": away_list, "away_abbr": away_abbr_list}
    df = pd.DataFrame(data=d)
    dataframe_cache[(year, week)] = df

    return df


# gathers a list of all teams abbreviations
def getonlyabbreviations(year):
    all_game_data = get_week_data(year, 1)
    unsplit = []
    abbreviations = []
    for x in all_game_data['events']:
        unsplit.append(x['shortName'])
    for matchup in unsplit:
        individual = matchup.replace(" VS ", " @ ").split(" @ ")
        for z in range(0, 2):
            abbreviations.append(individual[z])
    return abbreviations


def getonlyteams(year):
    all_game_data = get_week_data(year, 1)
    unsplit = []
    teams = []
    for x in all_game_data['events']:
        unsplit.append(x['name'])
    for matchup in unsplit:
        individual = matchup.split(" at ")
        for z in range(0, 2):
            teams.append(individual[z])
    return teams


def schedulesdf(year, team_abbr_list):

    cache_folder = "cache"
    cache_file = f"{cache_folder}/schedule_{year}.csv"

    # Create cache folder if it does not exist
    if not os.path.exists(cache_folder):
        os.makedirs(cache_folder)

    # Load saved schedule if it already exists
    if os.path.exists(cache_file):
        return pd.read_csv(cache_file)

    user_team = []
    home_away_list = []
    opponents = []
    week_list = []

    for team_abbr in team_abbr_list:

        for week in range(1, 19):
            week_list.append(week)
            user_team.append(team_abbr)

            games = gameidhomeaway(year, week)

            found = False

            for _, game in games.iterrows():
                if team_abbr == game['away_abbr']:
                    home_away_list.append("away")
                    opponents.append(game['home_abbr'])
                    found = True
                    break

                elif team_abbr == game['home_abbr']:
                    home_away_list.append("home")
                    opponents.append(game['away_abbr'])
                    found = True
                    break

            if not found:
                home_away_list.append("BYE")
                opponents.append("BYE")

    df_schedule = {
        "week": week_list,
        "user_team": user_team,
        "matchup": opponents,
        "home_away": home_away_list
    }

    df = pd.DataFrame(data=df_schedule)
    df = df.sort_values(["user_team", "week"])

    # Save schedule to CSV
    df.to_csv(cache_file, index=False)

    return df


def single_team_schedule(year, team_abbr):

    cache_folder = "cache"
    cache_file = f"{cache_folder}/schedule_{year}.csv"

    if os.path.exists(cache_file):
        df = pd.read_csv(cache_file)

    else:
        df = schedulesdf(year, getonlyabbreviations(year))

    team_schedule = df[df["user_team"] == team_abbr]

    return team_schedule


def week_opponent(year, week, team_abbr):
    team_schedule = single_team_schedule(year, team_abbr)
    opponent = team_schedule[team_schedule["week"] == week]
    return opponent["matchup"].iloc[0]


if __name__ == "__main__":
    for year in range(2021, 2026):
        for team in getonlyabbreviations(year):
            single_team_schedule(year, team)