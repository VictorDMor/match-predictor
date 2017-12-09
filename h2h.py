from stats import getTeamStats
import sqlite3
import pandas as pd

# Variable Initialization
######### Head to head array ###############
##       y = -1, 0, 1 = Draw              ##
##       y > 1 = Home victory             ## 
##       y < -1 = Away victory            ##
############################################


w_home = 1
w_points = 1
w_last_seven_points = 1
w_overall = 1
bias = 1

def HeadToHead(home_team, away_team, season, training=True):
	conn = sqlite3.connect('database.sqlite')
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
	home_team_id, away_team_id = teams_id['team_api_id'][0], teams_id['team_api_id'][1]

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
		return sum(head_to_head)+bias, head_to_head
	else:
		return sum(head_to_head)+bias