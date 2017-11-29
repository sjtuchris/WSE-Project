# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

class KickstarterProjectPipeline(object):
    def process_item(self, item, spider):
        with open("my_comment.txt",'a') as fp:
        	fp.write(item['project_url']+'\n')
        	fp.write(item['comment_num']+'\n')
        	fp.write(','.join(item['comment']) + '\n')

class MongoDBPipeline(object):

	def __init__(self):
		connection = pymongo.MongoClient(
			settings['MONGODB_SERVER'],
			settings['MONGODB_PORT']
		)
		db = connection[settings['MONGODB_DB']]
		self.collection = db[settings['MONGODB_COLLECTION']]

	def process_item(self, item, spider):
		valid = True
		for data in item:
			if not data:
				valid = False
				raise DropItem("Missing {0}!".format(data))
		if valid:
			# self.collection.insert(dict(item))
			self.collection.update_one(
				{"_id": item["project_url"]},
				{'$set':
					{
						"comment": item["comment"],
						"comment_num": item["comment_num"],
						"update": item["update"]
					}	
				}, upsert = True
			)
			log.msg("Project added to MongoDB!",
				level=log.DEBUG, spider=spider)
		return item
