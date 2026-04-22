import requests

def search_player(name):
    url = "https://site.web.api.espn.com/apis/common/v3/search"
    params = {
        "query": name,
        "limit": 5,
        "type": "player"
    }

    data = requests.get(url, params=params).json()

    players = data.get("items", [])

    for p in players:
        print(p["displayName"], "-", p.get("id"))

    return players[0]["id"] if players else None


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
        rank = stat.get("rankDisplayValue")

        if rank:
            print(f"{name}: {value} ({rank})")
        else:
            print(f"{name}: {value}")

# -------------------
# Example usage
# -------------------
player_name = "Jayden Daniels"

player_id = search_player(player_name)

if player_id:
    get_player_stats(player_id)
    get_player_stats(5306679)