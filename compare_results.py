import Schedule
import compare_teams
import real_results
import pickle
import random
import defensive
import fumbles
import interceptions
import kicking
import passing
import punting
import receiving
import rushing
from io import StringIO
import csv

stat_names = [
        "tackles",
        "solo",
        "dsacks",
        "tfl",
        "pd",
        "qb hits",
        "dtd",
        "fum",
        "lost",
        "no",
        "puyds",
        "puavg",
        "tb",
        "in 20",
        "pulong",
        "kpct",
        "klong",
        "kpts",
        "fg made",
        "fg att",
        "ex made",
        "ex att",
        "payds",
        "paavg",
        "patd",
        "paint",
        "pasacks",
        "pacomp",
        "paatt",
        "papct",
        "rerec",
        "reyds",
        "reavg",
        "retd",
        "relong",
        "retgts",
        "rucar",
        "ruyds",
        "ruavg",
        "rutd",
        "rulong",
        "intint",
        "intyds",
        "inttd"
    ]


score_cache = {}

for year in range(2021, 2026):
    with open(f"score_cache_{year}.pkl", "rb") as file:
        score_cache.update(pickle.load(file))


def compare_with_real(year, week, team, weights):
    main_score, opp_score = compare_teams.get_score(year, week, team, weights)  # only gathers one week, put into loop
    team_results = real_results.get_results(year, week, team)  # only gathers one, put in loop
    if team_results == "BYE":
        return "BYE"

    if main_score > opp_score:
        return "WIN"

    elif main_score < opp_score:
        return "LOSS"

    elif main_score == opp_score:
        return "TIE"

def get_percentage(mine, real):
    right = 0
    total = 0
    for item1, item2 in zip(mine, real):
        if item1 == item2:
            right += 1
    total += 1
    return right/total
def test_predictor(weights, return_results=False):

    amount_correct = 0
    amount_checked = 0

    game_results = []

    for game, data in score_cache.items():

        main_score = 0
        opp_score = 0

        for stat, result in data["comparisons"].items():

            if result is True:
                main_score += weights[stat]

            elif result is False:
                opp_score += weights[stat]

        if main_score > opp_score:
            prediction = "WIN"
        else:
            prediction = "LOSS"


        actual = data["result"]

        if prediction == actual:
            amount_correct += 1
            outcome = "CORRECT"
        else:
            outcome = "WRONG"

        amount_checked += 1

        game_results.append({
            "game": game,
            "main_score": main_score,
            "opp_score": opp_score,
            "prediction": prediction,
            "actual": actual,
            "result": outcome
        })


    accuracy = round(
        amount_correct / amount_checked * 100,
        2
    )

    if return_results:
        return accuracy, game_results

    return accuracy


def create_score_cache(year):

    cache = {}

    for team in Schedule.getonlyabbreviations(year):

        print(f"Caching {team}")

        for week in range(1, 19):

            result = real_results.get_results(
                year,
                week,
                team
            )

            # Skip bye weeks
            if result == "BYE":
                continue

            main, opp = compare_teams.gather_main_and_opponent_stats(
                year,
                week,
                team
            )

            comparison = compare_teams.compare_stats(
                main,
                opp
            )

            stat_comparisons = {}

            # Defensive
            stat_comparisons["tackles"] = defensive.compare_defensive_tackles(comparison)
            stat_comparisons["solo"] = defensive.compare_defensive_solo(comparison)
            stat_comparisons["dsacks"] = defensive.compare_defensive_sacks(comparison)
            stat_comparisons["tfl"] = defensive.compare_defensive_tfl(comparison)
            stat_comparisons["pd"] = defensive.compare_defensive_pd(comparison)
            stat_comparisons["qb hits"] = defensive.compare_defensive_qb_hits(comparison)
            stat_comparisons["dtd"] = defensive.compare_defensive_td(comparison)

            # Fumbles
            stat_comparisons["fum"] = fumbles.compare_fumbles_fum(comparison)
            stat_comparisons["lost"] = fumbles.compare_fumbles_lost(comparison)

            # Punting
            stat_comparisons["no"] = punting.compare_punting_no(comparison)
            stat_comparisons["puyds"] = punting.compare_punting_yds(comparison)
            stat_comparisons["puavg"] = punting.compare_punting_avg(comparison)
            stat_comparisons["tb"] = punting.compare_punting_TB(comparison)
            stat_comparisons["in 20"] = punting.compare_punting_in_20(comparison)
            stat_comparisons["pulong"] = punting.compare_punting_long(comparison)

            # Kicking
            stat_comparisons["kpct"] = kicking.compare_kicking_pct(comparison)
            stat_comparisons["klong"] = kicking.compare_kicking_long(comparison)
            stat_comparisons["kpts"] = kicking.compare_kicking_pts(comparison)
            stat_comparisons["fg made"] = kicking.compare_kicking_fg_made(comparison)
            stat_comparisons["fg att"] = kicking.compare_kicking_fg_att(comparison)
            stat_comparisons["ex made"] = kicking.compare_kicking_ex_made(comparison)
            stat_comparisons["ex att"] = kicking.compare_kicking_ex_att(comparison)

            # Passing
            stat_comparisons["payds"] = passing.compare_passing_yds(comparison)
            stat_comparisons["paavg"] = passing.compare_passing_avg(comparison)
            stat_comparisons["patd"] = passing.compare_passing_td(comparison)
            stat_comparisons["paint"] = passing.compare_passing_int(comparison)
            stat_comparisons["pasacks"] = passing.compare_passing_sacks(comparison)
            stat_comparisons["pacomp"] = passing.compare_passing_comp(comparison)
            stat_comparisons["paatt"] = passing.compare_passing_att(comparison)
            stat_comparisons["papct"] = passing.compare_passing_comp_pct(comparison)

            # Receiving
            stat_comparisons["rerec"] = receiving.compare_receiving_rec(comparison)
            stat_comparisons["reyds"] = receiving.compare_receiving_yds(comparison)
            stat_comparisons["reavg"] = receiving.compare_receiving_avg(comparison)
            stat_comparisons["retd"] = receiving.compare_receiving_td(comparison)
            stat_comparisons["relong"] = receiving.compare_receiving_long(comparison)
            stat_comparisons["retgts"] = receiving.compare_receiving_tgts(comparison)

            # Rushing
            stat_comparisons["rucar"] = rushing.compare_rushing_car(comparison)
            stat_comparisons["ruyds"] = rushing.compare_rushing_yds(comparison)
            stat_comparisons["ruavg"] = rushing.compare_rushing_avg(comparison)
            stat_comparisons["rutd"] = rushing.compare_rushing_td(comparison)
            stat_comparisons["rulong"] = rushing.compare_rushing_long(comparison)

            # Interceptions
            stat_comparisons["intint"] = interceptions.compare_interceptions_int(comparison)
            stat_comparisons["intyds"] = interceptions.compare_interceptions_yds(comparison)
            stat_comparisons["inttd"] = interceptions.compare_interceptions_td(comparison)


            cache[(year, week, team)] = {
                "comparisons": stat_comparisons,
                "result": result
            }


    with open(
        f"score_cache_{year}.pkl",
        "wb"
    ) as file:
        pickle.dump(
            cache,
            file
        )


    print("CACHE COMPLETE")

if __name__ == "__main__":
    # for years in range(2021, 2026):
    #     create_score_cache(years)

    random_tested = 0
    hill_tested = 0

    total_combinations = 1000000

    print("========== RANDOM SEARCH ==========")

    best_weights = None
    best_percentage = 0

    for i in range(total_combinations):

        weights = {
            stat: random.randint(0, 20)
            for stat in stat_names
        }

        percentage = test_predictor(weights)

        if percentage > best_percentage:
            best_percentage = percentage
            best_weights = weights.copy()

            print("\n***** NEW BEST *****")
            print(f"Accuracy: {best_percentage}%")
            print(best_weights)

        if random_tested % 100 == 0:
            print(f"Random Tested {random_tested}/{total_combinations}")

        random_tested += 1


    print("\n========== BEST WEIGHTS ==========")
    print(best_weights)
    print(f"Accuracy: {best_percentage}%")

    # ADD THIS HERE
    accuracy, results = test_predictor(best_weights, return_results=True)

    print("\n========== GAME RESULTS ==========")
    print(f"Accuracy: {accuracy}%")

    for game in results:
        print("-------------------------")
        print(game["game"])
        print("Scores:", game["main_score"], "-", game["opp_score"])
        print("Predicted:", game["prediction"])
        print("Actual:", game["actual"])
        print(game["result"])

    print("\n========== HILL CLIMB ==========")

    improved = True

    while improved:
        hill_tested += 1

        if hill_tested % 100 == 0:
            print(f"Hill Climb: {hill_tested} evaluations")
        improved = False

        for stat in stat_names:
            print(f"Optimizing {stat}...")
            current = best_weights[stat]

            for value in range(0, 6):

                if value == current:
                    continue

                candidate = best_weights.copy()
                candidate[stat] = value

                percentage = test_predictor(candidate)

                if percentage > best_percentage:
                    best_percentage = percentage
                    best_weights = candidate
                    improved = True

                    print(f"\nImproved to {best_percentage}%")
                    print(best_weights)

    print("\n===================================")
    print("SEARCH COMPLETE")
    print(f"Best Accuracy: {best_percentage}%")
    print("Best Weights:")
    print(best_weights)