import sys
import json
import glob, os
import time
import datetime

from csv import DictReader, writer
from pymongo import MongoClient

def getCsvFiles(cur_dir):
	res_files = [];
	for filename in glob.iglob(cur_dir + '**/*.csv', recursive=True):
		res_files.append(filename);
	return res_files;

def getUrlFromCsv(files):
	urls=[];
	for file in files:
		the_reader = DictReader(open(file, 'r'))
		for line_dict in the_reader:
			d = json.loads(line_dict['urls'])
			urls.append(d['web']['rewards'][:-7]+'comments');
	return urls

# Store all urls into a file
def writeUrl(files):
	# os.chdir("../")
	urls = getUrlFromCsv(files);
	with open("urls.txt",'a') as fp:
		for url in urls:
			fp.write(url + '\n');

# Store data in mongodb. In mongodb, those data will merge with crawled data
def writeMongo(files):
	client = MongoClient()
	db = client.kickstarter_db
	collection = db.projects

	for file in files:
		the_reader = DictReader(open(file, 'r'))
		for line_dict in the_reader:
			d = json.loads(line_dict['urls'])
			url = d['web']['rewards'][:-8];

			collection.update_one(
				{"_id": url},
				{'$set':
					{
						"name": line_dict['name'],
						"blurb": line_dict['blurb'],
						"goal": line_dict['goal'],
						"pledged": line_dict['pledged'],
						"state": line_dict['state'],
						"slug": line_dict['slug'],
						"disable_communication": line_dict['disable_communication'],
						"country": line_dict['country'],
						"currency": line_dict['currency'],
						"currency_symbol": line_dict['currency_symbol'],
						"currency_trailing_code": line_dict['currency_trailing_code'],
						"deadline": line_dict['deadline'],
						"state_changed_at": line_dict['state_changed_at'],
						"created_at": line_dict['created_at'],
						"launched_at": line_dict['launched_at'],
						# "staff_pick": line_dict['staff_pick'],
						# "is_starrable": line_dict['is_starrable'],
						"backers_count": line_dict['backers_count'],
						"usd_pledged": line_dict['usd_pledged'],
						# "converted_pledged_amount": line_dict['converted_pledged_amount'],
						# "current_currency": line_dict['current_currency'],
						# "usd_type": line_dict['usd_type'],
						"location": line_dict['location'],
						"category": line_dict['category'],
						"spotlight": line_dict['spotlight'],
					}
				}, upsert = True)
			print(line_dict['name']+' inserted!')

# Get the date that a project is fully pledged
def addSuccessDateMongo(files):
	client = MongoClient()
	db = client.kickstarter_db
	collection = db.projects
	url_success_dict = {}

	for file in files:
		the_reader = DictReader(open(file, 'r'))
		for line_dict in the_reader:
			d = json.loads(line_dict['urls'])
			url = d['web']['rewards'][:-8];

			fileDate = file.split('/')[-2].split('_')[1][:-3]
			timeStamp = time.mktime(datetime.datetime.strptime(fileDate, "%Y-%m-%d").timetuple())

			if float(line_dict['pledged'])>=float(line_dict['goal']):
				if url in url_success_dict:
					if timeStamp < url_success_dict[url]:
						url_success_dict[url] = timeStamp
						collection.update_one(
						{"_id": url},
						{'$set':
							{
								"success_date": str(timeStamp),
							}
						}, upsert = True)
						print(line_dict['name']+' updated')					
				else:
					url_success_dict[url] = timeStamp
					collection.update_one(
					{"_id": url},
					{'$set':
						{
							"success_date": str(timeStamp),
						}
					}, upsert = True)
					print(line_dict['name']+' updated')					

def writeMongoUSProjects(files):
	client = MongoClient()
	db = client.us_projects
	collection = db.projects

	for file in files:
		the_reader = DictReader(open(file, 'r'))
		for line_dict in the_reader:
			d = json.loads(line_dict['urls'])
			url = d['web']['rewards'][:-8];

			if line_dict['country'] == 'US':
				collection.update_one(
					{"_id": url},
					{'$set':
						{
							"blurb": line_dict['blurb'],
							"goal": line_dict['goal'],
							"pledged": line_dict['pledged'],
							"state": line_dict['state'],
							"country": line_dict['country'],
							"deadline": line_dict['deadline'],
							"launched_at": line_dict['launched_at'],
							"backers_count": line_dict['backers_count'],
							"usd_pledged": line_dict['usd_pledged'],						
							"location": line_dict['location'],
							"category": line_dict['category'],
							"creator": line_dict['creator'],
						}
					}, upsert = True)
				print(line_dict['name']+' inserted!')

def findCreator():
	file = "us_projects.csv"
	the_reader = DictReader(open(file, 'r'))
	creator_dict = {}
	for line_dict in the_reader:

		d = json.loads(line_dict['creator'])
		name = d['urls']['web']['user']
		success = line_dict['state']
		if name in creator_dict:
			pair = creator_dict[name]
			total = pair[0]+1
			success_sum = pair[1]
			if success == 'successful':
				success_sum = pair[1]+1
			creator_dict[name] = (total,success_sum)

		else:
			if success == 'successful':
				pair = (1,1)
			else:
				pair = (1,0)
			creator_dict[name] = pair
			# sortedDict = sorted(creator_dict, key=creator_dict.get, reverse=True)
	with open('creators.csv', 'w') as f:
		wtr = writer(f)
		for i in creator_dict:
			pair = creator_dict[i]
			wtr.writerow((i[36:],pair[0],pair[1],(1+pair[1])/(1+pair[0])))
			

def default():
	print("Invalid argument!")

def main():
	cur_dir = os.getcwd()+'/uncompress-data/';
	files = getCsvFiles(cur_dir);
	myCommandDict = {"writemongo": writeMongo(files), 
		"addsuccessrate": addSuccessDateMongo(files), 
		"writemongousprojects": writeMongoUSProjects(files), 
		"writeurls": writeUrl(files),
		"findCreator": findCreator(),
		"default": default()}
	commandline_args = sys.argv

	for argument in commandline_args[1]:
		if argument in myCommandDict:
			myCommandDict[argument]
		else:
			myCommandDict["default"]

if __name__ == "__main__":
	main()
