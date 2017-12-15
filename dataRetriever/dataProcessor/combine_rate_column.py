import json

from csv import DictReader,DictWriter

def loadCsv(file):
	csvReader = DictReader(open(file, 'r'))
	resDict = {}

	for line_dict in csvReader:
		keys = list(line_dict.keys())
		if keys[0] == 'rate':
			mainkey = keys[1]
		else:
			mainkey = keys[0]
		resDict[line_dict[mainkey]] = line_dict['rate']

	return resDict

# Add creator, state and subcategory success rate columns to training data
def merge():
	creator_dict = loadCsv("success_rate_creator.csv")
	state_dict = loadCsv("success_rate_state_us.csv")
	subcategory_dict = loadCsv("success_rate_subcategory.csv")

	project_reader = DictReader(open("us_projects.csv", 'r'))

	with open('train.csv', 'w') as f:  # Just use 'w' mode in 3.x
		flag = True
		for line_dict in project_reader:
			try:
				d=json.loads(line_dict['creator'])
				creator = d['urls']['web']['user']
				d=json.loads(line_dict['category'])
				subcategory = d['slug']
				d=json.loads(line_dict['location'])
				state = d['state']
				if line_dict['state']=="successful":
					line_dict['state']=1
				elif line_dict['state']=="failed":
					line_dict['state']=0
				else:
					continue


				line_dict['creator_rate'] = creator_dict[creator] if creator in creator_dict else 0.5
				line_dict['subcategory_rate'] = subcategory_dict[subcategory] if subcategory in subcategory_dict else 0.5
				line_dict['state_rate'] = state_dict[state] if state in state_dict else 0.5
				line_dict['period'] = (int(line_dict['deadline']) - int(line_dict['launched_at']))/60/60/24
				w = DictWriter(f, line_dict.keys())
				if flag == True:
					w.writeheader()
					flag = False

				w.writerow(line_dict)
			except Exception:
				pass

merge()