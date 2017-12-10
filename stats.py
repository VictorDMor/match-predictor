import sqlite3
import xml.etree.ElementTree as ET
import operator
import pandas as pd

def getTeamStats(home_team_id, away_team_id, initial_stage, final_stage, season, training=True):
	conn = sqlite3.connect('database.sqlite')
	home_stats = { 'home_wins': 0, 'home_draws': 0, 'home_losses': 0, 'home_goals_scored': 0, 'home_goals_conceded': 0 }
	away_stats = { 'away_wins': 0, 'away_draws': 0, 'away_losses': 0, 'away_goals_scored': 0, 'away_goals_conceded': 0 }
	home_at_home_stats = { 'home_at_home_wins': 0, 'home_at_home_draws': 0, 'home_at_home_losses': 0, 'home_at_home_goals_scored': 0, 'home_at_home_goals_conceded': 0 }
	home_at_away_stats = { 'home_at_away_wins': 0, 'home_at_away_draws': 0, 'home_at_away_losses': 0, 'home_at_away_goals_scored': 0, 'home_at_away_goals_conceded': 0 }
	away_at_home_stats = { 'away_at_home_wins': 0, 'away_at_home_draws': 0, 'away_at_home_losses': 0, 'away_at_home_goals_scored': 0, 'away_at_home_goals_conceded': 0 }
	away_at_away_stats = { 'away_at_away_wins': 0, 'away_at_away_draws': 0, 'away_at_away_losses': 0, 'away_at_away_goals_scored': 0, 'away_at_away_goals_conceded': 0 }
	winner_by_betting = 0

	#####################################################################################
	## Points, wins, draws, losses and attack/defense efficiency Function getTeamStats ##
	#####################################################################################
	teams_info = pd.read_sql_query("select team_long_name from Team where team_api_id in (" + str(home_team_id) + ", " + str(away_team_id) + ")", conn)
	home_team, away_team = teams_info["team_long_name"][0], teams_info["team_long_name"][1]

	home_scorers = {}
	away_scorers = {}

	if final_stage > 1:
		if not training:
			matches_before_round = pd.read_sql_query("select home_team_api_id, home_team_goal, away_team_api_id, away_team_goal, goal, B365H, B365D, B365A from Match " \
				"where country_id = 1729 and league_id = 1729 and season = '"+str(int(season)-1)+"/"+season+"' " \
				"and (home_team_api_id in ("+ str(home_team_id) +", "+ str(away_team_id) +") or away_team_api_id in ("+ str(home_team_id) +", "+ str(away_team_id) +")) " \
				"and stage between "+ str(initial_stage) +" and "+ str(final_stage), conn)
		else:
			matches_before_round = pd.read_sql_query("select home_team_api_id, home_team_goal, away_team_api_id, away_team_goal, goal, B365H, B365D, B365A from Match " \
				"where country_id = 1729 and league_id = 1729 and season = '"+ season +"' " \
				"and (home_team_api_id in ("+ str(home_team_id) +", "+ str(away_team_id) +") or away_team_api_id in ("+ str(home_team_id) +", "+ str(away_team_id) +")) " \
				"and stage between "+ str(initial_stage) +" and "+ str(final_stage), conn)

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

	return([home_stats, away_stats, home_scorers, away_scorers, home_points, away_points])