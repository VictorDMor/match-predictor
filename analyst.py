# Match Example: Liverpool x Chelsea (07/05/2017)
import sys
import pandas as pd
import sqlite3
import xml.etree.ElementTree as ET
import operator

conn = sqlite3.connect('database.sqlite')

if len(sys.argv) < 4:
	print("Lack of arguments")
	sys.exit()
else:
	home_team, away_team, season = sys.argv[1], sys.argv[2], sys.argv[3]

# Variable Initialization
home_lineup = []
away_lineup = []
home_rating_sum = 0
away_rating_sum = 0

# Useful functions

# Get team stats up to stage/round prior to the match

def getTeamStats(initial_stage, final_stage):
	matches_before_round = pd.read_sql_query("select * from Match where country_id = 1729 and league_id = 1729 and season = '"+str(int(season)-1)+"/"+season+"' and (home_team_api_id = "+ str(home_team_id) +" or home_team_api_id = "+ str(away_team_id) +" or away_team_api_id = "+ str(home_team_id) +" or away_team_api_id = "+ str(away_team_id) +") and stage >= "+ str(initial_stage) +" and stage < "+ str(final_stage), conn)
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
	home_scorers = {}
	away_scorers = {}
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
		match_goals_xml = ET.fromstring(matches_before_round['goal'][i])
		for scorer in match_goals_xml.findall("value"):
			if len(scorer.findall("player1")) != 0:
				player_name = pd.read_sql_query("select player_name from Player where player_api_id = "+ scorer.findall("player1")[0].text, conn)
				if scorer.findall("team")[0].text == str(home_team_id):
					if len(player_name) != 0:
						if player_name['player_name'][0] in home_scorers:
							home_scorers[player_name['player_name'][0]] += 1
						else:
							home_scorers[player_name['player_name'][0]] = 1
					else:
						if 'Unknown Player' in home_scorers:
							home_scorers['Unknown Player'] += 1
						else:
							home_scorers['Unknown Player'] = 1
				elif scorer.findall("team")[0].text == str(away_team_id):
					if len(player_name) != 0:
						if player_name['player_name'][0] in away_scorers:
							away_scorers[player_name['player_name'][0]] += 1
						else:
							away_scorers[player_name['player_name'][0]] = 1
					else:
						if 'Unknown Player' in away_scorers:
							away_scorers['Unknown Player'] += 1
						else:
							away_scorers['Unknown Player'] = 1


	home_points = home_stats['home_wins']*3+home_stats['home_draws']
	away_points = away_stats['away_wins']*3+away_stats['away_draws']

	print(home_team + " stats:")
	print("Wins: " + str(home_stats['home_wins']))
	print("Draws: " + str(home_stats['home_draws']))
	print("Losses: " + str(home_stats['home_losses']))
	print("Points: " + str(home_points))
	print("Goals scored: " + str(home_stats['home_goals_scored']))
	print("Goals conceded: " + str(home_stats['home_goals_conceded']) + "\n")
	print(away_team + " stats:")
	print("Wins: " + str(away_stats['away_wins']))
	print("Draws: " + str(away_stats['away_draws']))
	print("Losses: " + str(away_stats['away_losses']))
	print("Points: " + str(away_points))
	print("Goals scored: " + str(away_stats['away_goals_scored']))
	print("Goals conceded: " + str(away_stats['away_goals_conceded']) + "\n")

	return([home_stats, away_stats, home_scorers, away_scorers])

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
	+ " and season = '"+str(int(season)-1)+"/"+season+"'", conn)
match_round = match['stage'][0]
match_year = str(match['date'][0][:4])

# Step 3: Get team stats until that round
print("Team stats since round 1")
team_stats_all_matches = getTeamStats(1, match_round)
####################
# Last seven games #
####################

print("Team stats in the last seven matches")
team_stats_last_seven = getTeamStats(match_round-7, match_round)

#######################################################
## Attack/Defense efficiency - Function getTeamStats ##
#######################################################

###############################
# Line-ups and Rating Average #
###############################

for i in range(1, 12):
	home_player = pd.read_sql_query("select player_name from Player where player_api_id = "+ str(match['home_player_'+str(i)][0]), conn)
	home_player_rating = pd.read_sql_query("select overall_rating from Player_Attributes where player_api_id = " + str(match['home_player_'+str(i)][0]) + " and date like '"+ match_year +"%'", conn)
	if len(home_player_rating) == 0: # If player rating from the year when the match was realized not exists, gets most recent
		while len(home_player_rating) == 0:
			match_year = str(int(match_year)-1)
			home_player_rating = pd.read_sql_query("select overall_rating from Player_Attributes where player_api_id = " + str(match['home_player_'+str(i)][0]) + " and date like '"+ match_year +"%'", conn)
	away_player = pd.read_sql_query("select player_name from Player where player_api_id = "+ str(match['away_player_'+str(i)][0]), conn)
	away_player_rating = pd.read_sql_query("select overall_rating from Player_Attributes where player_api_id = " + str(match['away_player_'+str(i)][0]) + " and date like '"+ match_year +"%'", conn)
	if len(away_player_rating) == 0:
		while len(away_player_rating) == 0:
			match_year = str(int(match_year)-1)
			away_player_rating = pd.read_sql_query("select overall_rating from Player_Attributes where player_api_id = " + str(match['away_player_'+str(i)][0]) + " and date like '"+ match_year +"%'", conn)
	home_lineup.append([home_player['player_name'][0], home_player_rating['overall_rating'][0]])
	home_rating_sum += home_player_rating['overall_rating'][0]
	away_lineup.append([away_player['player_name'][0], away_player_rating['overall_rating'][0]])
	away_rating_sum += away_player_rating['overall_rating'][0]

print(home_team + " lineup: ")
for i in range(len(home_lineup)):
	if i == len(home_lineup)-1:
		print(home_lineup[i][0] + " - " + str(home_lineup[i][1]) + "\n")
	else:
		print(home_lineup[i][0] + " - " + str(home_lineup[i][1]))
print(away_team + " lineup: ")
for i in range(len(away_lineup)):
	if i == len(away_lineup)-1:
		print(away_lineup[i][0] + " - " + str(away_lineup[i][1]) + "\n")
	else:
		print(away_lineup[i][0] + " - " + str(away_lineup[i][1]))

print("Overall Rating")
print(home_team + ": " + str(home_rating_sum/11))
print(away_team + ": " + str(away_rating_sum/11) + "\n")

###############
# Goalscorers #
###############

home_goalscorers = sorted(team_stats_all_matches[2].items(), key=operator.itemgetter(1), reverse=True)
away_goalscorers = sorted(team_stats_all_matches[3].items(), key=operator.itemgetter(1), reverse=True)
print(home_team + " goalscorers: ")
for i in home_goalscorers:
	print(i[0] + " - " + str(i[1]))
print("\n" + away_team + " goalscorers: ")
for j in away_goalscorers:
	print(j[0] + " - " + str(j[1]))
