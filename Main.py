import PlayerID
import PlayerStats

if __name__ == "__main__":

    team = "Washington Commanders"
    df = PlayerID.show_team(team)
    stat_name_list = []
    count = 0
    for _, row in df.iterrows():
        player = row['player_id']

        stat_list = PlayerStats.get_player_stats(player)
        if stat_list is not None:
            for stat in stat_list:
                new = stat.split(":")[0].strip()

                if new not in stat_name_list:
                    stat_name_list.append(new)
                    count+=1
                    print(count)

    print(stat_name_list)