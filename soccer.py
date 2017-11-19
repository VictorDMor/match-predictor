from operator import itemgetter
import sqlite3
import pandas as pd
teams = []
conn = sqlite3.connect('database.sqlite')
english_matches = pd.read_sql_query("select season, (select t.team_long_name from Team t where t.team_api_id = m.home_team_api_id) as 'Time da Casa', \
	(select t.team_long_name from Team t where t.team_api_id = m.away_team_api_id) AwayTeamName, date as 'Data', stage as 'Rodada' from match m where country_id = 1729;", conn)
for i in range(len(english_matches)):
	if english_matches['Time da Casa'][i] not in teams:
		teams.append(english_matches['Time da Casa'][i])

sorted_teams = sorted(teams)

team_info = []
for i in sorted_teams:
	wins = 0
	draws = 0
	losses = 0
	goals_scored = 0
	matches = pd.read_sql_query("select season, (select t.team_long_name from Team t where t.team_api_id = m.home_team_api_id) as 'Time da Casa', home_team_goal, away_team_goal,\
	(select t.team_long_name from Team t where t.team_api_id = m.away_team_api_id) AwayTeamName, date as 'Data', stage as 'Rodada' from Match m where (m.away_team_api_id = (select t.team_api_id from Team t where t.team_long_name like '%"+i+"%') or \
	m.home_team_api_id = (select t.team_api_id from Team t where t.team_long_name like '%"+i+"%')) order by m.date asc", conn)
	for j in range(len(matches)):
		if (i in matches['Time da Casa'][j] and int(matches['home_team_goal'][j]) > int(matches['away_team_goal'][j])) | (i in matches['AwayTeamName'][j] and int(matches['away_team_goal'][j]) > int(matches['home_team_goal'][j])):
			wins += 1
			if(i in matches['Time da Casa'][j]):
				goals_scored += int(matches['home_team_goal'][j])
			else:
				goals_scored += int(matches['away_team_goal'][j])
		elif (i in matches['Time da Casa'][j] in i and int(matches['home_team_goal'][j]) < int(matches['away_team_goal'][j])) | (i in matches['AwayTeamName'][j] and int(matches['away_team_goal'][j]) < int(matches['home_team_goal'][j])):
			losses += 1
			if(i in matches['Time da Casa'][j]):
				goals_scored += int(matches['home_team_goal'][j])
			else:
				goals_scored += int(matches['away_team_goal'][j])
		else:
			draws += 1
			if(i in matches['Time da Casa'][j]):
				goals_scored += int(matches['home_team_goal'][j])
			else:
				goals_scored += int(matches['away_team_goal'][j])
	team_info.append({'Nome do time': i, 'Partidas':len(matches), 'Vitórias':wins, 'Empates':draws, 'Derrotas':losses, 'Pontos':wins*3+draws, 'Gols a favor':goals_scored})

final_team_info = sorted(team_info, key=itemgetter('Pontos'), reverse=True) 
count=1
for i in final_team_info:
	print(str(count) + '	' + i['Nome do time']+' '+str(i['Pontos'])+' '+str(i['Partidas'])+' '+str(i['Vitórias'])+' '+str(i['Empates'])+' '+str(i['Derrotas'])+' '+str(i['Gols a favor']))
	count+=1
conn.close()