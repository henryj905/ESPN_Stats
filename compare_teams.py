# given a team, gather their stats using weekly_stats
# using schedule, find their opponent
# using that opponent, gather their stats
# create new definition to compare their stats
import weekly_stats
import Schedule
import pandas as pd


def gather_main_and_opponent_stats(year, week, team_abbr):
    main_team_stat_list = []
    opponent_stat_list = []
    opponent = Schedule.week_opponent(year, week, team_abbr)

    if week > 18 or week < 1:
        raise(ValueError)

    # get the previous year
    elif week == 1:
        for game in range(1, 19):
            main_team_stat_list.append(weekly_stats.get_weekly_stats(year - 1, game, team_abbr))
            opponent_stat_list.append(weekly_stats.get_weekly_stats(year - 1, game, opponent))

    else:
        for game in range(1, week):
            main_team_stat_list.append(weekly_stats.get_weekly_stats(year, game, team_abbr))
            opponent_stat_list.append(weekly_stats.get_weekly_stats(year, game, opponent))

    combine_main = weekly_stats.combine_weekly_stats(main_team_stat_list)
    combine_opponent = weekly_stats.combine_weekly_stats(opponent_stat_list)

    return combine_main, combine_opponent


def compare_stats(main_stat_list, opponent_stat_list):

    comparison = {}

    for category in main_stat_list:

        main_df = main_stat_list[category]
        opp_df = opponent_stat_list[category]

        # Create a new dataframe to store True/False values
        result = pd.DataFrame()

        for column in main_df.columns:

            # Ignore identifying columns
            if column in ["team", "category"]:
                continue

            if column in opp_df.columns:

                main_value = main_df[column].iloc[0]
                opp_value = opp_df[column].iloc[0]

                result[column] = [
                    main_value > opp_value
                ]

        result.insert(
            0,
            "category",
            category
        )

        comparison[category] = result

    return comparison

def compare_defensive(TF_list):
    list = TF_list['defensive']
    list = list.drop(columns=['category'])
    value_true = 0
    value_false = 0
    for x in list:
        if list[x].iloc[0] == True:
            value_true = value_true + 1
        if list[x].iloc[0] == False:
            value_false = value_false + 1
    return value_true, value_false


def compare_fumbles(TF_list):
    list = TF_list['fumbles']
    list = list.drop(columns=['category'])
    value_true = 0
    value_false = 0
    for x in list:
        if list[x].iloc[0] == True:
            value_true = value_true + 1
        if list[x].iloc[0] == False:
            value_false = value_false + 1
    return value_true, value_false


def compare_kicking(TF_list):
    list = TF_list['kicking']
    list = list.drop(columns=['category'])
    value_true = 0
    value_false = 0
    for x in list:
        if list[x].iloc[0] == True:
            value_true = value_true + 1
        if list[x].iloc[0] == False:
            value_false = value_false + 1
    return value_true, value_false


def compare_passing(TF_list):
    list = TF_list['passing']
    list = list.drop(columns=['category'])
    value_true = 0
    value_false = 0
    for x in list:
        if list[x].iloc[0] == True:
            value_true = value_true + 1
        if list[x].iloc[0] == False:
            value_false = value_false + 1
    return value_true, value_false


def compare_punting(TF_list):
    list = TF_list['punting']
    list = list.drop(columns=['category'])
    value_true = 0
    value_false = 0
    for x in list:
        if list[x].iloc[0] == True:
            value_true = value_true + 1
        if list[x].iloc[0] == False:
            value_false = value_false + 1
    return value_true, value_false


def compare_receiving(TF_list):
    list = TF_list['receiving']
    list = list.drop(columns=['category'])
    value_true = 0
    value_false = 0
    for x in list:
        if list[x].iloc[0] == True:
            value_true = value_true + 1
        if list[x].iloc[0] == False:
            value_false = value_false + 1
    return value_true, value_false


def compare_rushing(TF_list):
    list = TF_list['rushing']
    list = list.drop(columns=['category'])
    value_true = 0
    value_false = 0
    for x in list:
        if list[x].iloc[0] == True:
            value_true = value_true + 1
        if list[x].iloc[0] == False:
            value_false = value_false + 1
    return value_true, value_false


def compare_interceptions(TF_list):
    list = TF_list['interceptions']
    list = list.drop(columns=['category'])
    value_true = 0
    value_false = 0
    for x in list:
        if list[x].iloc[0] == True:
            value_true = value_true + 1
        if list[x].iloc[0] == False:
            value_false = value_false + 1
    return value_true, value_false


def get_score(year, week, team):
    main, opp = gather_main_and_opponent_stats(2025, 1, "WSH")
    comparison = compare_stats(main, opp)

    compare_functions = {
        "passing": compare_passing,
        "rushing": compare_rushing,
        "receiving": compare_receiving,
        "defensive": compare_defensive,
        "kicking": compare_kicking,
        "punting": compare_punting
    }
    main_score = 0
    opp_score = 0
    for category, function in compare_functions.items():
        score1, score2 = function(
            comparison
        )
        main_score += score1
        opp_score += score2
    return main_score, opp_score
