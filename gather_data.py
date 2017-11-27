import csv
import tensorflow as tf

x = open("xs.csv", "r")
y = open("ys.csv", "r")
xs = []
ys = []
for line in x:
	if "\n" in line:
		new_line = line.replace("\n", "")
	xs_str = new_line.split(",")
	xs_int = []
	for i in xs_str:
		xs_int.append(int(i))
	xs.append(xs_int)
for line in y:
	ys.append(int(line))

print(xs)
print(ys)