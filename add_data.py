import sqlite3
import pandas as pd
conn = sqlite3.connect('database.sqlite')

f = open('E0.csv', 'r')
formatted_data = []
for line in f:
	line_array = line.split(',')
	formatted_date = '20'+line_array[1][6:]+line_array[1][3:5]+line_array[1][:2]

	if line_array[2] == 'Man City':
		home_team = 'Manchester City'
	elif line_array[2] == 'Man United':
		home_team = 'Manchester United'
	else:
		home_team = line_array[2]

	if line_array[3] == 'Man City':
		away_team = 'Manchester City'
	elif line_array[3] == 'Man United':
		away_team = 'Manchester United'
	else:
		away_team = line_array[3]

	home_team_id = pd.read_sql_query("select team_api_id from Team where team_long_name like '" + home_team + "%'", conn)
	away_team_id = pd.read_sql_query("select team_api_id from Team where team_long_name like '" + away_team + "%'", conn)
	sql = "INSERT into Match(country_id, league_id, season, stage, date, home_team_api_id, home_team_goal, away_team_goal, B365H, B365D, B365A)" + \
	"VALUES(1729, 1729, '2016/2017'"