import requests


passing = {
    'Passing Yards',
    'Passing Touchdowns',
    'Adjusted QBR',
}
rushing = {
    'Rushing Attempts',
    'Rushing Yards',
    'Rushing Touchdowns',
    'Yards Per Rush Attempt',
}
receiving = {
    'Receptions',
    'Receiving Yards',
    'Receiving Touchdowns',
    'Yards Per Reception',
}
defense = {
    'Solo Tackles',
    'Sacks',
    'Forced Fumbles',
    'Interceptions',
    'Passes Defended'
}
special = {
    'Field Goal Percentage',
    'Extra Point Percentage',
    'Long Field Goal Made',
    'Total Kicking Points',
    'Punts',
    'Gross Average Punt Yards',
    'Long Punt',
    'Punts Inside 20'
}


def get_player_stats(player_id):
    url = f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/{player_id}"

    data = requests.get(url).json()

    stats_summary = data.get("athlete", {}).get("statsSummary", {})

    stats = stats_summary.get("statistics", [])

    if not stats:
        return
    stats_list = []
    for stat in stats:
        name = stat.get("displayName", stat.get("name"))
        value = stat.get("displayValue")

        stats_list.append(f"{name}: {value}")
    return stats_list