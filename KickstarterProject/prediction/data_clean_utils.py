import csv

# Doing some data cleaning stuff
def success_fail_to_0_1():
	r = csv.reader(open('train.csv')) # Here your csv file
	w = csv.writer(open('new.csv', 'w'))
	lines = []
	for line in r:
		new_line = []
		if line[-1]!='successful' and line[-1]!='failed':
				continue
		for word in line:
			if word == "successful":
				new_line.append("1")
				continue
			elif word == "failed":
				new_line.append("-1")
				continue
			new_line.append(word)
		lines.append(new_line)
	w.writerows(lines)

def remove_null():
	r = csv.reader(open('train2.csv')) # Here your csv file
	w = csv.writer(open('new.csv', 'w'))
	lines = []
	for line in r:
		new_line = []
		null_flag = 0
		if line[-1]!='0' and line[-1]!='1' or len(line)!=7:
			continue

		for word in line:
			if word == "":
				null_flag = 1
				continue
			new_line.append(word)

		if null_flag==1:
			continue
		else:
			lines.append(new_line)
	w.writerows(lines)

remove_null()
