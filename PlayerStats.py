import requests

def get_player_stats(player_id):
    url = f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/{player_id}"

    data = requests.get(url).json()

    print("\n=== PLAYER STATS ===\n")

    # ✅ correct path (your actual structure)
    stats_summary = data.get("athlete", {}).get("statsSummary", {})

    stats = stats_summary.get("statistics", [])

    if not stats:
        print("No stats found.")
        return

    print(stats_summary.get("displayName", "Season Stats"), "\n")

    for stat in stats:
        name = stat.get("displayName", stat.get("name"))
        value = stat.get("displayValue")

        print(f"{name}: {value}")