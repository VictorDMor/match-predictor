# Match Example: Liverpool x Chelsea (07/05/2017)
import sys
import pandas as pd
import sqlite3

conn = sqlite3.connect('database.sqlite')

if len(sys.argv) < 3:
	print("Lack of arguments")
	sys.exit()
else:
	home_team, away_team = sys.argv[1], sys.argv[2]

# Useful functions

def getTeamStats(initial_stage, final_stage):
	matches_before_round = pd.read_sql_query("select * from Match where country_id = 1729 and league_id = 1729 and season = '2015/2016' and stage >= "+ str(initial_stage) +" and stage < "+ str(final_stage), conn)
	home_stats = {
		'home_wins': 0,
		'home_draws': 0,
		'home_losses': 0,
		'home_goals_scored': 0,
		'home_goals_conceded': 0
	}
	away_stats = {
		'away_wins': 0,
		'away_draws': 0,
		'away_losses': 0,
		'away_goals_scored': 0,
		'away_goals_conceded': 0
	}
	for i in range(len(matches_before_round)):
		if matches_before_round['home_team_api_id'][i] == home_team_id:
			if matches_before_round['home_team_goal'][i] > matches_before_round['away_team_goal'][i]:
				home_stats['home_wins'] += 1
			elif matches_before_round['home_team_goal'][i] == matches_before_round['away_team_goal'][i]:
				home_stats['home_draws'] += 1
			else:
				home_stats['home_losses'] += 1
			home_stats['home_goals_scored'] += matches_before_round['home_team_goal'][i]
			home_stats['home_goals_conceded'] += matches_before_round['away_team_goal'][i]
		elif matches_before_round['away_team_api_id'][i] == home_team_id:
			if matches_before_round['away_team_goal'][i] > matches_before_round['home_team_goal'][i]:
				home_stats['home_wins'] += 1
			elif matches_before_round['away_team_goal'][i] == matches_before_round['home_team_goal'][i]:
				home_stats['home_draws'] += 1
			else:
				home_stats['home_losses'] += 1
			home_stats['home_goals_scored'] += matches_before_round['away_team_goal'][i]
			home_stats['home_goals_conceded'] += matches_before_round['home_team_goal'][i]
		if matches_before_round['home_team_api_id'][i] == away_team_id:
			if matches_before_round['home_team_goal'][i] > matches_before_round['away_team_goal'][i]:
				away_stats['away_wins'] += 1
			elif matches_before_round['home_team_goal'][i] == matches_before_round['away_team_goal'][i]:
				away_stats['away_draws'] += 1
			else:
				away_stats['away_losses'] += 1
			away_stats['away_goals_scored'] += matches_before_round['home_team_goal'][i]
			away_stats['away_goals_conceded'] += matches_before_round['away_team_goal'][i]
		elif matches_before_round['away_team_api_id'][i] == away_team_id:
			if matches_before_round['away_team_goal'][i] > matches_before_round['home_team_goal'][i]:
				away_stats['away_wins'] += 1
			elif matches_before_round['away_team_goal'][i] == matches_before_round['home_team_goal'][i]:
				away_stats['away_draws'] += 1
			else:
				away_stats['away_losses'] += 1
			away_stats['away_goals_scored'] += matches_before_round['away_team_goal'][i]
			away_stats['away_goals_conceded'] += matches_before_round['home_team_goal'][i]

	home_points = home_stats['home_wins']*3+home_stats['home_draws']
	away_points = away_stats['away_wins']*3+away_stats['away_draws']

	print(home_team + " stats:")
	print("Wins: " + str(home_stats['home_wins']))
	print("Draws: " + str(home_stats['home_draws']))
	print("Losses: " + str(home_stats['home_losses']))
	print("Points: " + str(home_points) + "\n")
	print("Goals scored: " + str(home_stats['home_goals_scored']))
	print("Goals conceded: " + str(home_stats['home_goals_conceded']) + "\n")
	print(away_team + " stats:")
	print("Wins: " + str(away_stats['away_wins']))
	print("Draws: " + str(away_stats['away_draws']))
	print("Losses: " + str(away_stats['away_losses']))
	print("Points: " + str(away_points) + "\n")
	print("Goals scored: " + str(away_stats['away_goals_scored']))
	print("Goals conceded: " + str(away_stats['away_goals_conceded']) + "\n")

	return([home_stats, away_stats])

################################
# League position of each team #
################################

# Step 1: Get Team IDs

home_team_id = pd.read_sql_query("select team_api_id from Team where team_long_name like '" + home_team + "%'", conn)['team_api_id'][0]
away_team_id = pd.read_sql_query("select team_api_id from Team where team_long_name like '" + away_team + "%'", conn)['team_api_id'][0]

print("Team IDs")
print(home_team + ": " + str(home_team_id))
print(away_team + ": " + str(away_team_id) +"\n")

# Step 2: Get match in question to get round
match = pd.read_sql_query("select * from Match where home_team_api_id = "+ str(home_team_id) + " and away_team_api_id = "+ str(away_team_id)\
	+ " and season = '2015/2016'", conn)
match_round = match['stage'][0]

# Step 3: Get team stats until that round
getTeamStats(1, match_round)
####################
# Last seven games #
####################

getTeamStats(match_round-7, match_round)

#############################
# Attack/Defense efficiency #
#############################

