# Match Example: Liverpool x Chelsea (07/05/2017)
import sys
import os
import csv
from h2h import HeadToHead
from training import NetworkTraining

os.remove("xs.csv")
os.remove("ys.csv")

if len(sys.argv) < 4:
	print("Lack of arguments")
	sys.exit()
else:
	home_team, away_team, season = sys.argv[1], sys.argv[2], sys.argv[3]

xs = open('xs.csv', 'w')
ys = open('ys.csv', 'w')

winner = HeadToHead(season, False, home_team, away_team)
if winner >= 1:
	print("Winner will be: " + home_team + "\n")
elif winner < 0:
	print("Winner will be: " + away_team + "\n")
else:
	print("The match will end as a draw! \n")

hits, misses, x, y = NetworkTraining()

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