import Schedule
import compare_teams
import real_results
import pickle


with open("score_cache.pkl", "rb") as file:
    score_cache = pickle.load(file)


def compare_with_real(year, week, team, weights):
    main_score, opp_score = compare_teams.get_score(year, week, team, weights)  # only gathers one week, put into loop
    team_results = real_results.get_results(year, week, team)  # only gathers one, put in loop
    if team_results == "BYE":
        return "BYE"

    if main_score > opp_score:
        if team_results == "WIN":
            return "WIN"
        else:
            return "LOSE"
    elif main_score < opp_score:
        if team_results == "LOSE":
            return "WIN"
        else:
            return "LOSE"
    elif main_score == opp_score:
        if team_results == "TIE":
            return "WIN"
        else:
            return "LOSE"

def test_predictor(weights):

    amount_correct = 0
    amount_checked = 0

    for game, data in score_cache.items():

        main_score = 0
        opp_score = 0

        for category, scores in data["scores"].items():

            score1, score2 = scores

            main_score += score1 * weights[category]
            opp_score += score2 * weights[category]


        if main_score > opp_score:
            prediction = "WIN"
        else:
            prediction = "LOSE"


        if prediction == data["result"]:
            amount_correct += 1

        amount_checked += 1


    return round(
        amount_correct / amount_checked * 100,
        2
    )


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

            category_scores = {}

            # Store the unweighted scores
            for category in comparison:

                if category == "passing":
                    category_scores["passing"] = compare_teams.compare_passing(comparison)

                elif category == "rushing":
                    category_scores["rushing"] = compare_teams.compare_rushing(comparison)

                elif category == "receiving":
                    category_scores["receiving"] = compare_teams.compare_receiving(comparison)

                elif category == "defensive":
                    category_scores["defensive"] = compare_teams.compare_defensive(comparison)

                elif category == "fumbles":
                    category_scores["fumbles"] = compare_teams.compare_fumbles(comparison)

                elif category == "interceptions":
                    category_scores["interceptions"] = compare_teams.compare_interceptions(comparison)

                elif category == "kicking":
                    category_scores["kicking"] = compare_teams.compare_kicking(comparison)

                elif category == "punting":
                    category_scores["punting"] = compare_teams.compare_punting(comparison)


            cache[(year, week, team)] = {
                "scores": category_scores,
                "result": result
            }


    with open(
        "score_cache.pkl",
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
    best_percentage = 0
    best_weights = None

    combinations_tested = 0

    for passing in range(1, 6):
        for rushing in range(1, 6):
            for receiving in range(1, 6):
                for defensive in range(1, 6):
                    for fumbles in range(1, 6):
                        for interceptions in range(1, 6):
                            for kicking in range(1, 6):
                                for punting in range(1, 6):

                                    weights = {
                                        "passing": passing,
                                        "rushing": rushing,
                                        "receiving": receiving,
                                        "defensive": defensive,
                                        "fumbles": fumbles,
                                        "interceptions": interceptions,
                                        "kicking": kicking,
                                        "punting": punting
                                    }

                                    combinations_tested += 1

                                    percentage = test_predictor(weights)
                                    total_combinations = 5 ** 8
                                    if combinations_tested % 100 == 0:
                                        print(
                                            f"Tested {combinations_tested}/{total_combinations}"
                                        )

                                    if percentage > best_percentage:
                                        best_percentage = percentage
                                        best_weights = weights.copy()

                                        print("***** NEW BEST FOUND! *****")
                                        print(f"Accuracy: {best_percentage}%")
                                        print(best_weights)

    print("\n===================================")
    print("SEARCH COMPLETE")
    print(f"Combinations Tested: {combinations_tested}")
    print(f"Best Accuracy: {best_percentage}%")
    print("Best Weights:")
    print(best_weights)