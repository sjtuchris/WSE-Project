import sys
from pyspark import SparkContext
from operator import add
import csv
import json

# dumbass shit environment
class DataSummary:

    def __init__(self, input_file, output_file):
        self.sc = SparkContext()
        self.input_file = input_file
        self.output_file = output_file

    # util
    def readfile(self, input):
        csvreader = csv.reader(input)
        next(csvreader)
        return csvreader

    def convert_ts_to_datetime(self, input):
        return ""

    def format_result(self, res):
        return "%s\t%s" % (res[0], res[1])

    # mappers
    # by country
    def by_country(self, input): # list with multiple column, country: 9
        return input[9], 1  # abbr or full name

    def by_city(self,  input):
        location = input[26]
        location_json = json.load(location)
        return location["displayable_name"], 1

    # by state success or fail
    def by_state(self, input):
        return input[6], 1

    # by success backers
    def by_backer(self, input):
        return input[19], 1

    def by_category(self, input):
        # handle json
        input_json = json.load(input[27])
        subcategory = input_json["slug"]
        return subcategory[subcategory.rfind('/')+1:], 1

    def by_subcategory(self, input):
        input_json = json.load(input[27])
        return input_json["slug"], 1

    def by_pledged(self, input):
        return input[5]

    def by_start_date(self, input):
        return ""

    #  filters
    def success_state(self, input):
        return input[6] == "successful"

    # main
    def main(self):
        kickstarter_data = self.sc.textFile("/user/cl3869/uncompress-data/Kickstarter_2017-01-15T22_21_04_985Z/Kickstarter.csv", use_unicode=False).mapPartitions(readfile)
        by_state = kickstarter_data.map(self.by_state).reduceByKey(add).map(self.format_result)
        by_state.saveAsTextFile(self.output_file+"/"+"by_state")
        sc.stop()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: inputfile outputfile"
        exit(-1)

    ds = DataSummary(sys.argv[1], sys.argv[2])
    ds.main()
