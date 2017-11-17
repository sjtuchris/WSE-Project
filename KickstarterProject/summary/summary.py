import sys
# import os
from pyspark import SparkContext
from operator import add
import csv
import json


# util
def readfile(input):
    csvreader = csv.reader(input)
    next(csvreader)
    return csvreader


def convert_ts_to_datetime(input):
    return ""


def format_result(res):
    return "%s\t%s" % (res[0], res[1])


# mappers
# by country
def by_country(input): # list with multiple column, country: 9
    return input[9] # abbr or full name


def by_city(input):
    location = input[26]
    location_json = json.load(location)
    return location["displayable_name"]


# by state success or fail
def by_state(input):
    return input[6], 0


# by success backers
def by_backer(input):
    return input[19]


def by_category(input):
    # handle json
    input_json = json.load(input[27])
    subcategory = input_json["slug"]
    return subcategory[subcategory.rfind('/')+1:]


def by_subcategory(input):
    input_json = json.load(input[27])
    return input_json["slug"]


def by_pledged(input):
    return input[5]

def by_start_date(input):

#  filters
def success_state(input):
    return input[6] == "successful"


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: inputfile outputfile"
        exit(-1)

    sc = SparkContext()
    # read from folder
    kickstarter_data = sc.wholeTextFiles(sys.argv[1]).mapPartitions(readfile)
    by_state = statekickstarter_data.map(by_state).reduceByKey(add).map(format_result)
    by_state.saveAsTextFile(sys.argv[2]+"/"+"by_state")
    sc.stop()

