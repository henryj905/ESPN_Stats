import PlayerID
import PlayerStats

if __name__ == "__main__":
    team = input("Team? city and team first letter caps\n")
    print(PlayerID.show_team(team))
    player = input("\nPlayer full name (first letter caps):\n")
    id = PlayerID.get_player_id(player)
    print(id)

    print(PlayerStats.get_player_stats(id))