#coding=utf8
import sys
from pyspark import SparkContext
from operator import add
import csv
import json


class DataSummary:

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    # util
    def readfile(self, input):
        csv.field_size_limit(sys.maxsize)
        csvreader = csv.reader(input, quoting=csv.QUOTE_ALL)
        next(csvreader)
        return csvreader

    def convert_ts_to_datetime(self, input):
        return ""

    def format_result(self, res):
        return "%s\t%s" % (res[0], res[1])

    # mappers
    # by country
    def by_country(self, input): # list with multiple column, country: 9
        return input[6], 1  # abbr or full name
    #
    # def by_state(self, input):
    #     # onpy apply for us
    #     if input[6] == "US":
    #         return "dummy", 1
    #     else:
    #         return "", 0

    def by_city(self,  input):
        try:
            location = input[15]
            location_json = json.loads(location)
            return location_json["name"], 1
        except:
            return "dummy", 1

    def by_us_states(self, input):
        try:
            location = input[15]
            location_json = json.loads(location)
            return location_json["state"], 1
        except:
            return "dummy", 1

    # by state success or fail
    def by_state(self, input):
        return input[20], 1

    # by backers
    def by_backer(self, input): # [www.baidu.com, 120, 20,..]
        return input[20], int(input[1]) # key, value

    # by comment number
    def by_comment_num(self, input):
        try:
            return input[20], int(input[5])
        except:
            return input[20], 0

    def by_category(self, input):
        # handle json
        input_json = json.loads(input[3])
        subcategory = input_json["slug"]
        return subcategory[:subcategory.rfind('/')], 1

    def by_subcategory(self, input):
        input_json = json.loads(input[3])
        return input_json["slug"], 1

    def by_pledged(self, input):
        return input[20], float(input[17])

    def by_goal(self, input):
        return input[20], float(input[13])

    def by_duration(self, input):
        #deadline = datetime.datetime.fromtimestamp(int(input[11])) # utc or not probably doesnt matter, in terms of days
        #launch_at = datetime.datetime.fromtimestamp(int(input[14]))
        #return (deadline - launch_at).days, 1
        return input[20], int((int(input[11]) - int(input[14]))/86400)

    def by_update(self, input):
        try:
            return input[20], int(input[22])
        except:
            return input[20], 0

    #  filters
    def filter_success(self, input):
        return input[20] == "successful"

    def filter_failed(self, input):
        return input[20] == "failed"

    def filter_us(self, input):
        try:
            location = input[15]
            location_json = json.loads(location)
            return location_json["country"] == "US"
        except:
            return False


# main
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: inputfile outputfile"
        exit(-1)
    csv.field_size_limit(sys.maxsize)
    ds = DataSummary(sys.argv[1], sys.argv[2])

    sc = SparkContext()
    kickstarter_data = sc.textFile(sys.argv[1], use_unicode=False).mapPartitions(ds.readfile)
    # status of projects
    by_state = kickstarter_data.map(ds.by_state).reduceByKey(add).map(ds.format_result)
    by_state.saveAsTextFile(ds.output_file+"/"+"by_state")
    # by backers
    by_backers = kickstarter_data.map(ds.by_backer).reduceByKey(add).map(ds.format_result)
    by_backers.saveAsTextFile(ds.output_file+"/by_backers")
    # by pledged
    by_pledged = kickstarter_data.map(ds.by_pledged).reduceByKey(add).map(ds.format_result)
    by_pledged.saveAsTextFile(ds.output_file + "/by_pledged")
    # by goal
    by_goal = kickstarter_data.map(ds.by_goal).reduceByKey(add).map(ds.format_result)
    by_goal.saveAsTextFile(ds.output_file + "/by_goal")
    # by comment number
    by_comment = kickstarter_data.map(ds.by_comment_num).reduceByKey(add).map(ds.format_result)
    by_comment.saveAsTextFile(ds.output_file + "/by_comment_num")
    # by category
    by_category = kickstarter_data.map(ds.by_category).reduceByKey(add).map(ds.format_result)
    by_category.saveAsTextFile(ds.output_file + "/by_category")
    # by sub category
    by_sub_category = kickstarter_data.map(ds.by_subcategory).reduceByKey(add).map(ds.format_result)
    by_sub_category.saveAsTextFile(ds.output_file + "/by_sub_category")
    # by successful category, in order to caculate successful rate on each category
    by_success_category = kickstarter_data.filter(ds.filter_success).map(ds.by_category).reduceByKey(add).map(ds.format_result)
    by_success_category.saveAsTextFile(ds.output_file + "/by_success_category")
    # by failed category
    by_fail_category = kickstarter_data.filter(ds.filter_failed).map(ds.by_category).reduceByKey(add).map(ds.format_result)
    by_fail_category.saveAsTextFile(ds.output_file + "/by_fail_category")
    # by successful sub category
    by_success_subcategory = kickstarter_data.filter(ds.filter_success).map(ds.by_subcategory).reduceByKey(add).map(ds.format_result)
    by_success_subcategory.saveAsTextFile(ds.output_file + "/by_success_subcategory")
    # by failed sub category
    by_fail_subcategory = kickstarter_data.filter(ds.filter_failed).map(ds.by_subcategory).reduceByKey(add).map(ds.format_result)
    by_fail_subcategory.saveAsTextFile(ds.output_file + "/by_fail_subcategory")
    # by_country
    by_country = kickstarter_data.map(ds.by_country).reduceByKey(add).map(ds.format_result)
    by_country.saveAsTextFile(ds.output_file + "/by_country")
    # by city
    by_city = kickstarter_data.map(ds.by_city).reduceByKey(add).map(ds.format_result)
    by_city.saveAsTextFile(ds.output_file + "/by_city")
    #by us states
    by_us_states = kickstarter_data.filter(ds.filter_us).map(ds.by_us_states).reduceByKey(add).map(ds.format_result)
    by_us_states.saveAsTextFile(ds.output_file + "/by_us_states")
    #average duration for each success project
    by_duration = kickstarter_data.filter(ds.filter_success).map(ds.by_duration).reduceByKey(add).map(ds.format_result)
    by_duration.saveAsTextFile(ds.output_file + "/by_duration")

    # by updates
    by_update = kickstarter_data.map(ds.by_update).reduceByKey(add).map(ds.format_result)
    by_update.saveAsTextFile(ds.output_file + "/by_update")

    sc.stop()
