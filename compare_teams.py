# given a team, gather their stats using weekly_stats
# using schedule, find their opponent
# using that opponent, gather their stats
# create new definition to compare their stats
import defensive
import fumbles
import interceptions
import kicking
import passing
import punting
import receiving
import rushing
import weekly_stats
import Schedule
import team_stats
import real_results
import pandas as pd
import os


def gather_main_and_opponent_stats(year, week, team_abbr):
    main_team_stat_list = []
    opponent_stat_list = []
    opponent = Schedule.week_opponent(year, week, team_abbr)

    if week > 18 or week < 1:
        raise(ValueError)

    # get the previous year
    elif week == 1:

        combine_main = team_stats.get_team_stats(
            year - 1,
            team_abbr
        )

        combine_opponent = team_stats.get_team_stats(
            year - 1,
            opponent
        )

        return combine_main, combine_opponent

    else:
        for game in range(1, week):
            main_team_stat_list.append(weekly_stats.get_weekly_stats(year, game, team_abbr))
            opponent_stat_list.append(weekly_stats.get_weekly_stats(year, game, opponent))

    combine_main = weekly_stats.combine_weekly_stats(main_team_stat_list)
    combine_opponent = weekly_stats.combine_weekly_stats(opponent_stat_list)

    return combine_main, combine_opponent


def get_cached_weekly_stats(year, week, team_abbr):

    week_folder = os.path.join(
        "player_stats_cache",
        f"player_stats_cache_{year}",
        f"player_stats_cache_{year}_{week}"
    )

    if not os.path.exists(week_folder):
        return {}

    stats = {}

    for file in os.listdir(week_folder):

        if not file.endswith(".csv"):
            continue

        category = file.replace(".csv", "")

        path = os.path.join(
            week_folder,
            file
        )

        df = pd.read_csv(path)

        if "team" in df.columns:
            df = df[df["team"] == team_abbr]

        stats[category] = df.reset_index(drop=True)

    return stats

def compare_stats(main_stat_list, opponent_stat_list):

    comparison = {}

    for category in main_stat_list:

        if category not in opponent_stat_list:
            continue

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


def get_score(year, week, team, multipliers=None):

    result = real_results.get_results(year, week, team)

    if result == "BYE":
        return 0, 0

    if multipliers is None:
        multipliers = {
            "tackles": 1,
            "solo": 1,
            "dsacks": 1,
            "tfl": 1,
            "pd": 1,
            "qb hits": 1,
            "dtd": 1,
            "fum": 1,
            "lost": 1,
            "no": 1,
            "puyds": 1,
            "puavg": 1,
            "tb": 1,
            "in 20": 1,
            "pulong": 1,
            "kpct": 1,
            "klong": 1,
            "kpts": 1,
            "fg made": 1,
            "fg att": 1,
            "ex made": 1,
            "ex att": 1,
            "payds": 1,
            "paavg": 1,
            "patd": 1,
            "paint": 1,
            "pasacks": 1,
            "pacomp": 1,
            "paatt": 1,
            "papct": 1,
            "rerec": 1,
            "reyds": 1,
            "reavg": 1,
            "retd": 1,
            "relong": 1,
            "retgts": 1,
            "rucar": 1,
            "ruyds": 1,
            "ruavg": 1,
            "rutd": 1,
            "rulong": 1,
            "intint": 1,
            "intyds": 1,
            "inttd": 1
        }

    main, opp = gather_main_and_opponent_stats(year, week, team)
    comparison = compare_stats(main, opp)

    main_score = 0
    opp_score = 0
    if defensive.compare_defensive_tackles(comparison) == True:
        main_score += 1 * multipliers['tackles']
    elif defensive.compare_defensive_tackles(comparison) == False:
        opp_score += 1 * multipliers['tackles']
    else:
        pass

    if defensive.compare_defensive_solo(comparison) == True:
        main_score += 1 * multipliers['solo']
    elif defensive.compare_defensive_solo(comparison) == False:
        opp_score += 1 * multipliers['solo']
    else:
        pass

    if defensive.compare_defensive_sacks(comparison) == True:
        main_score += 1 * multipliers['dsacks']
    elif defensive.compare_defensive_sacks(comparison) == False:
        opp_score += 1 * multipliers['dsacks']
    else:
        pass

    if defensive.compare_defensive_tfl(comparison) == True:
        main_score += 1 * multipliers['tfl']
    elif defensive.compare_defensive_tfl(comparison) == False:
        opp_score += 1 * multipliers['tfl']
    else:
        pass

    if defensive.compare_defensive_pd(comparison) == True:
        main_score += 1 * multipliers['pd']
    elif defensive.compare_defensive_pd(comparison) == False:
        opp_score += 1 * multipliers['pd']
    else:
        pass

    if defensive.compare_defensive_qb_hits(comparison) == True:
        main_score += 1 * multipliers['qb hits']
    elif defensive.compare_defensive_qb_hits(comparison) == False:
        opp_score += 1 * multipliers['qb hits']
    else:
        pass

    if defensive.compare_defensive_td(comparison) == True:
        main_score += 1 * multipliers['dtd']
    elif defensive.compare_defensive_td(comparison) == False:
        opp_score += 1 * multipliers['dtd']
    else:
        pass

    if fumbles.compare_fumbles_fum(comparison) == True:
        main_score += 1 * multipliers['fum']
    elif fumbles.compare_fumbles_fum(comparison) == False:
        opp_score += 1 * multipliers['fum']
    else:
        pass

    if fumbles.compare_fumbles_lost(comparison) == True:
        main_score += 1 * multipliers['lost']
    elif fumbles.compare_fumbles_lost(comparison) == False:
        opp_score += 1 * multipliers['lost']
    else:
        pass

    if punting.compare_punting_no(comparison) == True:
        main_score += 1 * multipliers['no']
    elif punting.compare_punting_no(comparison) == False:
        opp_score += 1 * multipliers['no']
    else:
        pass

    if punting.compare_punting_yds(comparison) == True:
        main_score += 1 * multipliers['puyds']
    elif punting.compare_punting_yds(comparison) == False:
        opp_score += 1 * multipliers['puyds']
    else:
        pass

    if punting.compare_punting_avg(comparison) == True:
        main_score += 1 * multipliers['puavg']
    elif punting.compare_punting_avg(comparison) == False:
        opp_score += 1 * multipliers['puavg']
    else:
        pass

    if punting.compare_punting_TB(comparison) == False:
        main_score += 1 * multipliers['tb']
    elif punting.compare_punting_TB(comparison) == True:
        opp_score += 1 * multipliers['tb']
    else:
        pass

    if punting.compare_punting_in_20(comparison) == True:
        main_score += 1 * multipliers['in 20']
    elif punting.compare_punting_in_20(comparison) == False:
        opp_score += 1 * multipliers['in 20']
    else:
        pass

    if punting.compare_punting_long(comparison) == True:
        main_score += 1 * multipliers['pulong']
    elif punting.compare_punting_long(comparison) == False:
        opp_score += 1 * multipliers['pulong']
    else:
        pass

    if kicking.compare_kicking_pct(comparison) == True:
        main_score += 1 * multipliers['kpct']
    elif kicking.compare_kicking_pct(comparison) == False:
        opp_score += 1 * multipliers['kpct']
    else:
        pass

    if kicking.compare_kicking_long(comparison) == True:
        main_score += 1 * multipliers['klong']
    elif kicking.compare_kicking_long(comparison) == False:
        opp_score += 1 * multipliers['klong']
    else:
        pass

    if kicking.compare_kicking_pts(comparison) == True:
        main_score += 1 * multipliers['kpts']
    elif kicking.compare_kicking_pts(comparison) == False:
        opp_score += 1 * multipliers['kpts']
    else:
        pass

    if kicking.compare_kicking_fg_made(comparison) == True:
        main_score += 1 * multipliers['fg made']
    elif kicking.compare_kicking_fg_made(comparison) == False:
        opp_score += 1 * multipliers['fg made']
    else:
        pass

    if kicking.compare_kicking_fg_att(comparison) == True:
        main_score += 1 * multipliers['fg att']
    elif kicking.compare_kicking_fg_att(comparison) == False:
        opp_score += 1 * multipliers['fg att']
    else:
        pass

    if kicking.compare_kicking_ex_made(comparison) == True:
        main_score += 1 * multipliers['ex made']
    elif kicking.compare_kicking_ex_made(comparison) == False:
        opp_score += 1 * multipliers['ex made']
    else:
        pass

    if kicking.compare_kicking_ex_att(comparison) == True:
        main_score += 1 * multipliers['ex att']
    elif kicking.compare_kicking_ex_att(comparison) == False:
        opp_score += 1 * multipliers['ex att']
    else:
        pass

    if passing.compare_passing_yds(comparison) == True:
        main_score += 1 * multipliers['payds']
    elif passing.compare_passing_yds(comparison) == False:
        opp_score += 1 * multipliers['payds']
    else:
        pass

    if passing.compare_passing_avg(comparison) == True:
        main_score += 1 * multipliers['paavg']
    elif passing.compare_passing_avg(comparison) == False:
        opp_score += 1 * multipliers['paavg']
    else:
        pass

    if passing.compare_passing_td(comparison) == True:
        main_score += 1 * multipliers['patd']
    elif passing.compare_passing_td(comparison) == False:
        opp_score += 1 * multipliers['patd']
    else:
        pass

    if passing.compare_passing_int(comparison) == True:
        main_score += 1 * multipliers['paint']
    elif passing.compare_passing_int(comparison) == False:
        opp_score += 1 * multipliers['paint']
    else:
        pass

    if passing.compare_passing_sacks(comparison) == True:
        main_score += 1 * multipliers['pasacks']
    elif passing.compare_passing_sacks(comparison) == False:
        opp_score += 1 * multipliers['pasacks']
    else:
        pass

    if passing.compare_passing_comp(comparison) == True:
        main_score += 1 * multipliers['pacomp']
    elif passing.compare_passing_comp(comparison) == False:
        opp_score += 1 * multipliers['pacomp']
    else:
        pass

    if passing.compare_passing_att(comparison) == True:
        main_score += 1 * multipliers['paatt']
    elif passing.compare_passing_att(comparison) == False:
        opp_score += 1 * multipliers['paatt']
    else:
        pass

    if passing.compare_passing_comp_pct(comparison) == True:
        main_score += 1 * multipliers['papct']
    elif passing.compare_passing_comp_pct(comparison) == False:
        opp_score += 1 * multipliers['papct']
    else:
        pass

    if receiving.compare_receiving_rec(comparison) == True:
        main_score += 1 * multipliers['rerec']
    elif receiving.compare_receiving_rec(comparison) == False:
        opp_score += 1 * multipliers['rerec']
    else:
        pass

    if receiving.compare_receiving_yds(comparison) == True:
        main_score += 1 * multipliers['reyds']
    elif receiving.compare_receiving_yds(comparison) == False:
        opp_score += 1 * multipliers['reyds']
    else:
        pass

    if receiving.compare_receiving_avg(comparison) == True:
        main_score += 1 * multipliers['reavg']
    elif receiving.compare_receiving_avg(comparison) == False:
        opp_score += 1 * multipliers['reavg']
    else:
        pass

    if receiving.compare_receiving_td(comparison) == True:
        main_score += 1 * multipliers['retd']
    elif receiving.compare_receiving_td(comparison) == False:
        opp_score += 1 * multipliers['retd']
    else:
        pass

    if receiving.compare_receiving_long(comparison) == True:
        main_score += 1 * multipliers['relong']
    elif receiving.compare_receiving_long(comparison) == False:
        opp_score += 1 * multipliers['relong']
    else:
        pass

    if receiving.compare_receiving_tgts(comparison) == True:
        main_score += 1 * multipliers['retgts']
    elif receiving.compare_receiving_tgts(comparison) == False:
        opp_score += 1 * multipliers['retgts']
    else:
        pass

    if rushing.compare_rushing_car(comparison) == True:
        main_score += 1 * multipliers['rucar']
    elif rushing.compare_rushing_car(comparison) == False:
        opp_score += 1 * multipliers['rucar']
    else:
        pass

    if rushing.compare_rushing_yds(comparison) == True:
        main_score += 1 * multipliers['ruyds']
    elif rushing.compare_rushing_yds(comparison) == False:
        opp_score += 1 * multipliers['ruyds']
    else:
        pass

    if rushing.compare_rushing_avg(comparison) == True:
        main_score += 1 * multipliers['ruavg']
    elif rushing.compare_rushing_avg(comparison) == False:
        opp_score += 1 * multipliers['ruavg']
    else:
        pass

    if rushing.compare_rushing_td(comparison) == True:
        main_score += 1 * multipliers['rutd']
    elif rushing.compare_rushing_td(comparison) == False:
        opp_score += 1 * multipliers['rutd']
    else:
        pass

    if rushing.compare_rushing_long(comparison) == True:
        main_score += 1 * multipliers['rulong']
    elif rushing.compare_rushing_long(comparison) == False:
        opp_score += 1 * multipliers['rulong']
    else:
        pass

    if interceptions.compare_interceptions_int(comparison) == True:
        main_score += 1 * multipliers['intint']
    elif interceptions.compare_interceptions_int(comparison) == False:
        opp_score += 1 * multipliers['intint']
    else:
        pass

    if interceptions.compare_interceptions_yds(comparison) == True:
        main_score += 1 * multipliers['intyds']
    elif interceptions.compare_interceptions_yds(comparison) == False:
        opp_score += 1 * multipliers['intyds']
    else:
        pass

    if interceptions.compare_interceptions_td(comparison) == True:
        main_score += 1 * multipliers['inttd']
    elif interceptions.compare_interceptions_td(comparison) == False:
        opp_score += 1 * multipliers['inttd']
    else:
        pass

    return main_score, opp_score
