import json
import glob, os

from csv import DictReader
from pymongo import MongoClient

def getCsvFiles(cur_dir):
	# os.chdir("./test")
	# sub_dirs = [x[0] for x in os.walk('./test')]
	# files = []
	# for file in glob.glob("*.csv"):
 	#  		files.append(file)
	# return files

	# root_dir = '/Users/Chris/DEV/kickstarter_project/data/test/'
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


def writeUrl(files):
	# os.chdir("../")
	urls = getUrlFromCsv(files);
	with open("urls.txt",'a') as fp:
		for url in urls:
			fp.write(url + '\n');

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

# cur_dir = os.getcwd()+'/test/';
cur_dir = os.getcwd()+'/uncompress-data/';
files = getCsvFiles(cur_dir);
writeMongo(files);
