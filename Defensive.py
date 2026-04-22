import requests
#https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={401772718}
def get_game_summary(game_id):
    url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={game_id}"
    return requests.get(url).json()

tags = (get_game_summary(401772718))

next = (tags['boxscore']['players'])


Stat_type_list = []
stats = ''
for item in next:
    stats = (item['statistics'])
stat_list = []
player_stat = []
for Stat_type in stats:
    for stat in (Stat_type['keys']):
        stat_list.append(stat)
    for num in (Stat_type['athletes']):
        for athlete, statistics in zip(num['athlete'], num['stats']):
            athleteName = num['athlete']['firstName'], num['athlete']['lastName']
            player_stat.append([athleteName , statistics])
for stat, player in zip(stat_list, player_stat):
    print(stat, player)
    # for type, person in zip(stat_list, player_stat):
    #     print(type, person)
# # for item in stats:
# #     for item2 in (item['athletes']):
# #         print(item2['stats'])
# #         print(item2['athlete']['displayName'])
#
# last = ''
# for item in stats:
#     last = item
# for key in last['athletes']:
#     print(key)