import requests
import json
import time
import os

BASE = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"
CACHE_FILE = "nfl_players_simple.json"

# -----------------------------
# STEP 1: SCRAPE PLAYERS
# -----------------------------
if not os.path.exists(CACHE_FILE):

    seen_players = set()
    all_players = []

    for week in range(1, 19):
        print(f"Getting week {week}...")

        scoreboard = requests.get(
            f"{BASE}/scoreboard?week={week}&seasontype=2"
        ).json()

        for event in scoreboard.get("events", []):

            summary = requests.get(
                f"{BASE}/summary?event={event['id']}"
            ).json()

            players = summary.get("boxscore", {}).get("players", [])

            for team in players:
                team_name = team["team"]["displayName"]

                for stat_group in team.get("statistics", []):

                    for athlete in stat_group.get("athletes", []):

                        player = athlete.get("athlete", {})

                        player_id = player.get("id")

                        # avoid duplicates
                        if player_id in seen_players:
                            continue

                        seen_players.add(player_id)

                        all_players.append({
                            "player_id": player_id,
                            "player_name": player.get("displayName"),
                            "team": team_name
                        })

        time.sleep(0.3)

    with open(CACHE_FILE, "w") as f:
        json.dump(all_players, f, indent=2)

    print("Done scraping players.")