import pandas as pd
import json

def get_df():
    CACHE_FILE = 'nfl_players_simple.json'
    with open(CACHE_FILE, "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    return df

def show_team(team):
    df = get_df()

    df = df[df['team'] == team]

    return df.sort_values(['player_name'])
def get_player_id(player_name):
    df = get_df()

    df = df[df['player_name']==player_name]
    result = df.loc[df['player_name'] == player_name, 'player_id']

    return result.iloc[0]
