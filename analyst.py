# Match Example: Liverpool x Chelsea (07/05/2017)
import sys
import pandas as pd
import sqlite3
import xml.etree.ElementTree as ET
import operator
import os
import csv

conn = sqlite3.connect('database.sqlite')

os.remove("xs.csv")
os.remove("ys.csv")

if len(sys.argv) < 4:
	print("Lack of arguments")
	sys.exit()
else:
	home_team, away_team, season = sys.argv[1], sys.argv[2], sys.argv[3]


# Variable Initialization
######### Head to head array ###############
##       y = -1, 0, 1 = Draw              ##
##       y > 1 = Home victory             ## 
##       y < -1 = Away victory            ##
############################################
x = []
y = []
xs = open('xs.csv', 'w')
ys = open('ys.csv', 'w')
w_home = 1
w_points = 1
w_last_seven_points = 1
w_overall = 1
bias = 1

# Useful functions

### Get team stats up to stage/round prior to the match

def getTeamStats(home_team_id, away_team_id, initial_stage, final_stage, season, training=True):
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
	home_at_home_stats = {
		'home_at_home_wins': 0,
		'home_at_home_draws': 0,
		'home_at_home_losses': 0,
		'home_at_home_goals_scored': 0,
		'home_at_home_goals_conceded': 0
	}
	home_at_away_stats = {
		'home_at_away_wins': 0,
		'home_at_away_draws': 0,
		'home_at_away_losses': 0,
		'home_at_away_goals_scored': 0,
		'home_at_away_goals_conceded': 0
	}
	away_at_home_stats = {
		'away_at_home_wins': 0,
		'away_at_home_draws': 0,
		'away_at_home_losses': 0,
		'away_at_home_goals_scored': 0,
		'away_at_home_goals_conceded': 0
	}
	away_at_away_stats = {
		'away_at_away_wins': 0,
		'away_at_away_draws': 0,
		'away_at_away_losses': 0,
		'away_at_away_goals_scored': 0,
		'away_at_away_goals_conceded': 0
	}

	#####################################################################################
	## Points, wins, draws, losses and attack/defense efficiency Function getTeamStats ##
	#####################################################################################
	home_team = pd.read_sql_query("select * from Team where team_api_id = " + str(home_team_id), conn)['team_long_name'][0]
	away_team = pd.read_sql_query("select * from Team where team_api_id = " + str(away_team_id), conn)['team_long_name'][0]

	home_scorers = {}
	away_scorers = {}

	if final_stage > 1:
		if not training:
			matches_before_round = pd.read_sql_query("select * from Match where country_id = 1729 and league_id = 1729 and season = '"+str(int(season)-1)+"/"+season+"' and (home_team_api_id = "+ str(home_team_id) +" or home_team_api_id = "+ str(away_team_id) +" or away_team_api_id = "+ str(home_team_id) +" or away_team_api_id = "+ str(away_team_id) +") and stage >= "+ str(initial_stage) +" and stage < "+ str(final_stage), conn)
		else:
			matches_before_round = pd.read_sql_query("select * from Match where country_id = 1729 and league_id = 1729 and season = '"+ season +"' and (home_team_api_id = "+ str(home_team_id) +" or home_team_api_id = "+ str(away_team_id) +" or away_team_api_id = "+ str(home_team_id) +" or away_team_api_id = "+ str(away_team_id) +") and stage >= "+ str(initial_stage) +" and stage < "+ str(final_stage), conn)

		for i in range(len(matches_before_round)): # Loops in all matches played by those teams in EPL before analysed match
			if matches_before_round['home_team_api_id'][i] == home_team_id: # If home team of match analysed was home team in the ith match
				if matches_before_round['home_team_goal'][i] > matches_before_round['away_team_goal'][i]:
					home_stats['home_wins'] += 1
					home_at_home_stats['home_at_home_wins'] += 1
				elif matches_before_round['home_team_goal'][i] == matches_before_round['away_team_goal'][i]:
					home_stats['home_draws'] += 1
					home_at_home_stats['home_at_home_draws'] += 1
				else:
					home_stats['home_losses'] += 1
					home_at_home_stats['home_at_home_losses'] += 1
				home_stats['home_goals_scored'] += matches_before_round['home_team_goal'][i]
				home_stats['home_goals_conceded'] += matches_before_round['away_team_goal'][i]
				home_at_home_stats['home_at_home_goals_scored'] += matches_before_round['home_team_goal'][i]
				home_at_home_stats['home_at_home_goals_conceded'] += matches_before_round['away_team_goal'][i]
			elif matches_before_round['away_team_api_id'][i] == home_team_id: # If home team of match analysed was away team in the ith match
				if matches_before_round['away_team_goal'][i] > matches_before_round['home_team_goal'][i]:
					home_stats['home_wins'] += 1
					home_at_away_stats['home_at_away_wins'] += 1
				elif matches_before_round['away_team_goal'][i] == matches_before_round['home_team_goal'][i]:
					home_stats['home_draws'] += 1
					home_at_away_stats['home_at_away_draws'] += 1
				else:
					home_stats['home_losses'] += 1
					home_at_away_stats['home_at_away_losses'] += 1
				home_stats['home_goals_scored'] += matches_before_round['away_team_goal'][i]
				home_stats['home_goals_conceded'] += matches_before_round['home_team_goal'][i]
				home_at_away_stats['home_at_away_goals_scored'] += matches_before_round['away_team_goal'][i]
				home_at_away_stats['home_at_away_goals_conceded'] += matches_before_round['home_team_goal'][i]
			if matches_before_round['home_team_api_id'][i] == away_team_id: # If away team of match analysed was home team in the ith match
				if matches_before_round['home_team_goal'][i] > matches_before_round['away_team_goal'][i]:
					away_stats['away_wins'] += 1
					away_at_home_stats['away_at_home_wins'] += 1
				elif matches_before_round['home_team_goal'][i] == matches_before_round['away_team_goal'][i]:
					away_stats['away_draws'] += 1
					away_at_home_stats['away_at_home_draws'] += 1
				else:
					away_stats['away_losses'] += 1
					away_at_home_stats['away_at_home_losses'] += 1
				away_stats['away_goals_scored'] += matches_before_round['home_team_goal'][i]
				away_stats['away_goals_conceded'] += matches_before_round['away_team_goal'][i]
				away_at_home_stats['away_at_home_goals_scored'] += matches_before_round['away_team_goal'][i]
				away_at_home_stats['away_at_home_goals_conceded'] += matches_before_round['home_team_goal'][i]
			elif matches_before_round['away_team_api_id'][i] == away_team_id: # If away team of match analysed was away team in the ith match
				if matches_before_round['away_team_goal'][i] > matches_before_round['home_team_goal'][i]:
					away_stats['away_wins'] += 1
					away_at_away_stats['away_at_away_wins'] += 1
				elif matches_before_round['away_team_goal'][i] == matches_before_round['home_team_goal'][i]:
					away_stats['away_draws'] += 1
					away_at_away_stats['away_at_away_draws'] += 1
				else:
					away_stats['away_losses'] += 1
					away_at_away_stats['away_at_away_losses'] += 1
				away_stats['away_goals_scored'] += matches_before_round['away_team_goal'][i]
				away_stats['away_goals_conceded'] += matches_before_round['home_team_goal'][i]
				away_at_away_stats['away_at_away_goals_scored'] += matches_before_round['away_team_goal'][i]
				away_at_away_stats['away_at_away_goals_conceded'] += matches_before_round['home_team_goal'][i]

			match_goals_xml = ET.fromstring(matches_before_round['goal'][i]) # Goalscorers of the ith match
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

		home_goalscorers = sorted(home_scorers.items(), key=operator.itemgetter(1), reverse=True)
		away_goalscorers = sorted(away_scorers.items(), key=operator.itemgetter(1), reverse=True)


	home_points = home_stats['home_wins']*3+home_stats['home_draws']
	home_at_home_points = home_at_home_stats['home_at_home_wins']*3+home_at_home_stats['home_at_home_draws']
	home_at_away_points = home_at_away_stats['home_at_away_wins']*3+home_at_away_stats['home_at_away_draws']
	away_points = away_stats['away_wins']*3+away_stats['away_draws']
	away_at_home_points = away_at_home_stats['away_at_home_wins']*3+away_at_home_stats['away_at_home_draws']
	away_at_away_points = away_at_away_stats['away_at_away_wins']*3+away_at_away_stats['away_at_away_draws']

	# print(home_team + " stats:")
	# print("Overall:")
	# print("Wins: " + str(home_stats['home_wins']))
	# print("Draws: " + str(home_stats['home_draws']))
	# print("Losses: " + str(home_stats['home_losses']))
	# print("Points: " + str(home_points))
	# print("Goals scored: " + str(home_stats['home_goals_scored']))
	# print("Goals conceded: " + str(home_stats['home_goals_conceded']) + "\n")
	# print("At home:")
	# print("Wins: " + str(home_at_home_stats['home_at_home_wins']))
	# print("Draws: " + str(home_at_home_stats['home_at_home_draws']))
	# print("Losses: " + str(home_at_home_stats['home_at_home_losses']))
	# print("Points: " + str(home_at_home_points))
	# print("Goals scored: " + str(home_at_home_stats['home_at_home_goals_scored']))
	# print("Goals conceded: " + str(home_at_home_stats['home_at_home_goals_conceded']) + "\n")
	# print("Away:")
	# print("Wins: " + str(home_at_away_stats['home_at_away_wins']))
	# print("Draws: " + str(home_at_away_stats['home_at_away_draws']))
	# print("Losses: " + str(home_at_away_stats['home_at_away_losses']))
	# print("Points: " + str(home_at_away_points))
	# print("Goals scored: " + str(home_at_away_stats['home_at_away_goals_scored']))
	# print("Goals conceded: " + str(home_at_away_stats['home_at_away_goals_conceded']) + "\n")
	# print(away_team + " stats:")
	# print("Overall:")
	# print("Wins: " + str(away_stats['away_wins']))
	# print("Draws: " + str(away_stats['away_draws']))
	# print("Losses: " + str(away_stats['away_losses']))
	# print("Points: " + str(away_points))
	# print("Goals scored: " + str(away_stats['away_goals_scored']))
	# print("Goals conceded: " + str(away_stats['away_goals_conceded']) + "\n")
	# print("At home:")
	# print("Wins: " + str(away_at_home_stats['away_at_home_wins']))
	# print("Draws: " + str(away_at_home_stats['away_at_home_draws']))
	# print("Losses: " + str(away_at_home_stats['away_at_home_losses']))
	# print("Points: " + str(away_at_home_points))
	# print("Goals scored: " + str(away_at_home_stats['away_at_home_goals_scored']))
	# print("Goals conceded: " + str(away_at_home_stats['away_at_home_goals_conceded']) + "\n")
	# print("Away:")
	# print("Wins: " + str(away_at_away_stats['away_at_away_wins']))
	# print("Draws: " + str(away_at_away_stats['away_at_away_draws']))
	# print("Losses: " + str(away_at_away_stats['away_at_away_losses']))
	# print("Points: " + str(away_at_away_points))
	# print("Goals scored: " + str(away_at_away_stats['away_at_away_goals_scored']))
	# print("Goals conceded: " + str(away_at_away_stats['away_at_away_goals_conceded']) + "\n")

	return([home_stats, away_stats, home_scorers, away_scorers, home_points, away_points])

def NetworkTraining():
	matches = pd.read_sql_query("select * from Match where country_id = 1729 and league_id = 1729", conn)
	hits = 0
	misses = 0
	for i in range(len(matches)):
		if i % 3039 == 0:
			print("Hits: " + str(hits))
			print("Misses: " + str(misses))
			if i != 0:
				print("Accuracy: " + str((float(hits)/float(hits+misses))*100))
		home_team = pd.read_sql_query("select * from Team where team_api_id = " + str(matches['home_team_api_id'][i]), conn)['team_long_name'][0]
		away_team = pd.read_sql_query("select * from Team where team_api_id = " + str(matches['away_team_api_id'][i]), conn)['team_long_name'][0]
		match_hh = []
		predicted_winner = HeadToHead(home_team, away_team, str(matches['season'][i]))
		if matches['home_team_goal'][i] > matches['away_team_goal'][i]:
			match_hh.append(1)
		elif matches['home_team_goal'][i] < matches['away_team_goal'][i]:
			match_hh.append(-1)
		else:
			match_hh.append(0)
		if (sum(match_hh) >= 1 and predicted_winner >= 1) or (sum(match_hh) < 0 and predicted_winner < 0) or (sum(match_hh) == 0 and predicted_winner == 0):
			hits += 1
		else:
			misses += 1

		y.append(match_hh)
	return hits, misses

def HeadToHead(home_team, away_team, season, training=True):
	home_rating_sum = 0
	away_rating_sum = 0
	home_lineup = []
	away_lineup = []
	head_to_head = [1*w_home]
	################################
	# League position of each team #
	################################

	# Step 1: Get Team IDs
	teams_id = pd.read_sql_query("select team_api_id from Team where team_long_name like '" + home_team + "%' or team_long_name like '" + away_team + "%'", conn)
	home_team_id = teams_id['team_api_id'][0]
	away_team_id = teams_id['team_api_id'][1]

	# Step 2: Get match in question to get round
	if not training:
		match = pd.read_sql_query("select * from Match where home_team_api_id = "+ str(home_team_id) + " and away_team_api_id = "+ str(away_team_id)\
			+ " and season = '"+str(int(season)-1)+"/"+season+"'", conn)
	else:
		match = pd.read_sql_query("select * from Match where home_team_api_id = "+ str(home_team_id) + " and away_team_api_id = "+ str(away_team_id)\
			+ " and season = '"+season+"'", conn)
	match_round = match['stage'][0]
	match_year = str(match['date'][0][:4])

	# Step 3: Get team stats until that round
	team_stats_all_matches = getTeamStats(home_team_id, away_team_id, 1, match_round, season, training)
	####################
	# Last seven games #
	####################
	team_stats_last_seven = getTeamStats(home_team_id, away_team_id, match_round-7, match_round, season, training)

	###############################
	# Line-ups and Rating Average #
	###############################

	home_lineup_string = ''
	away_lineup_string = ''
	for i in range(1, 12):
		if i == 1:
			if match['home_player_'+str(i)][0] is not None:
				home_lineup_string += "select player_name from Player where player_api_id = "+ str(match['home_player_'+str(i)][0]) + " "
			if match['away_player_'+str(i)][0] is not None:
				away_lineup_string += "select player_name from Player where player_api_id = "+ str(match['away_player_'+str(i)][0]) + " "
		else:
			if match['home_player_'+str(i)][0] is not None:
				home_lineup_string += "or player_api_id = "+ str(match['home_player_'+str(i)][0]) + " "
			if match['away_player_'+str(i)][0] is not None:
				away_lineup_string += "or player_api_id = "+ str(match['away_player_'+str(i)][0]) + " "

	home_players = pd.read_sql_query(home_lineup_string, conn)

	away_players = pd.read_sql_query(away_lineup_string, conn)

	for i in range(0, len(home_players)):
		if match['home_player_'+str(i+1)][0] is not None:
			home_player_rating = pd.read_sql_query("select overall_rating from Player_Attributes where player_api_id = " + str(match['home_player_'+str(i+1)][0]) + " and date like '"+ match_year +"%'", conn)
			if len(home_player_rating) == 0: # If player rating from the year when the match was realized not exists, gets most recent
				while len(home_player_rating) == 0:
					match_year = str(int(match_year)-1)
					home_player_rating = pd.read_sql_query("select overall_rating from Player_Attributes where player_api_id = " + str(match['home_player_'+str(i+1)][0]) + " and date like '"+ match_year +"%'", conn)
			home_lineup.append([home_players['player_name'][i], home_player_rating['overall_rating'][0]])
			home_rating_sum += home_player_rating['overall_rating'][0]
		else:
			home_lineup.append(["Unknown Player", home_rating_sum/i])
			home_rating_sum += home_rating_sum/i

	for i in range(0, len(away_players)):
		if match['away_player_'+str(i+1)][0] is not None:
			away_player_rating = pd.read_sql_query("select overall_rating from Player_Attributes where player_api_id = " + str(match['away_player_'+str(i+1)][0]) + " and date like '"+ match_year +"%'", conn)
			if len(away_player_rating) == 0:
				while len(away_player_rating) == 0:
					match_year = str(int(match_year)-1)
					away_player_rating = pd.read_sql_query("select overall_rating from Player_Attributes where player_api_id = " + str(match['away_player_'+str(i+1)][0]) + " and date like '"+ match_year +"%'", conn)
			away_lineup.append([away_players['player_name'][i], away_player_rating['overall_rating'][0]])
			away_rating_sum += away_player_rating['overall_rating'][0]
		else:
			away_lineup.append(["Unknown Player", away_rating_sum/i])
			away_rating_sum += away_rating_sum/i

	# print("Overall Rating")
	# print(home_team + ": " + str(home_rating_sum/11))
	# print(away_team + ": " + str(away_rating_sum/11) + "\n")

	############################################
	# LET'S GET READY TO RUMBLE! HEAD TO HEAD! #
	############################################

	# Points (overall)
	home_points = team_stats_all_matches[4]
	away_points = team_stats_all_matches[5]

	if home_points > away_points:
		head_to_head.append(1*w_home)
	elif home_points < away_points:
		head_to_head.append(-1*w_home)
	else:
		head_to_head.append(0)

	# Points (last seven)
	home_points_last_seven = team_stats_last_seven[4]
	away_points_last_seven = team_stats_last_seven[5]

	if home_points_last_seven > away_points_last_seven:
		head_to_head.append(1*w_last_seven_points)
	elif home_points_last_seven < away_points_last_seven:
		head_to_head.append(-1*w_last_seven_points)
	else:
		head_to_head.append(0)

	# Rating
	home_overall_rating = home_rating_sum/len(home_players)
	away_overall_rating = away_rating_sum/len(away_players)

	if home_overall_rating > away_overall_rating:
		head_to_head.append(1*w_overall)
	elif home_overall_rating < away_overall_rating:
		head_to_head.append(-1*w_overall)
	else:
		head_to_head.append(0)
	if training:
		x.append(head_to_head)
	return sum(head_to_head)+bias

winner = HeadToHead(home_team, away_team, season, False)
if winner >= 1:
	print("Winner will be: " + home_team + "\n")
elif winner < 0:
	print("Winner will be: " + away_team + "\n")
else:
	print("The match will end as a draw! \n")

hits, misses = NetworkTraining()

with open('xs.csv', 'w') as xs:
	writer = csv.writer(xs)
	for i in x:
		writer.writerow(i)

with open('ys.csv', 'w') as ys:
	writer = csv.writer(ys)
	for i in y:
		writer.writerow(i)

print("Hits: " + str(hits))
print("Misses: " + str(misses))
print("Accuracy: " + str((float(hits)/float(hits+misses))*100))