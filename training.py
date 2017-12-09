import sqlite3
import pandas as pd
from h2h import HeadToHead

def NetworkTraining():
	conn = sqlite3.connect('database.sqlite')
	matches = pd.read_sql_query("select home_team_api_id, away_team_api_id, home_team_goal, away_team_goal, season from Match where country_id = 1729 and league_id = 1729", conn)
	hits = 0
	misses = 0
	x = []
	y = []
	for i in range(len(matches)):
		team_names = pd.read_sql_query("select team_long_name from Team where team_api_id in (" + str(matches['home_team_api_id'][i]) + ", " + str(matches['away_team_api_id'][i]) + ")", conn)
		home_team, away_team = team_names['team_long_name'][0], team_names['team_long_name'][1]
		match_hh = []
		predicted_winner, match_x = HeadToHead(home_team, away_team, str(matches['season'][i]))
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

		if i % 1 == 0:
			print("Hits: " + str(hits))
			print("Misses: " + str(misses))
			print("Accuracy: " + str((float(hits)/float(hits+misses))*100))

		x.append(match_x)
		y.append(match_hh)
	return hits, misses, x, y