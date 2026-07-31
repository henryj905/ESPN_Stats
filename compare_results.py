import compare_teams
import real_results

def compare_with_real(year, week, team):
    main_score, opp_score = compare_teams.get_score(year, week, team)



if __name__ == "__main__":
    print(compare_with_real(2025, 1, "WSH"))