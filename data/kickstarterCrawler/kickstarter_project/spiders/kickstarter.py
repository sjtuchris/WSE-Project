# -*- coding: utf-8 -*-
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from kickstarter_project.items import KickstarterProjectItem

class KickstarterSpider(CrawlSpider):
	name = 'kickstarter'
	allowed_domains = ['kickstarter.com']
	# start_urls = []

	custom_settings = {
		'CONCURRENT_REQUESTS': 20,
		'DOWNLOAD_DELAY': 0.2,
		'AUTOTHROTTLE_ENABLED': False,
		'RANDOMIZE_DOWNLOAD_DELAY': False
	}

	# def start_requests(self):
	# 	# start_urls = [
	# 	# 	'https://www.kickstarter.com/projects/831231712/prepare-for-takeoff-with-robynn-shayne/comments',
	# 	# 	'https://www.kickstarter.com/projects/704738550/knox-county-jug-stompers-new-album-preorder/comments'
	# 	# ]
	# 	start_urls = self.load_urls()
	# 	return [ Request(url = start_url) for start_url in start_urls ]

	# def __init__(self):
	# 	self.start_urls = self.load_urls();

	def start_requests(self):
		return [Request(i.strip(), callback=self.parse) for i in open('urls.txt').readlines()]

	def parse(self, response):
		comments_count = response.xpath('//div[@class="project-nav__links"]//a/@data-comments-count')
		comments = response.xpath('//ol[@class="list-comments click"]//p//text()')
		updates = response.xpath('//div[@class="project-nav__links"]//a[@class="js-load-project-content js-load-project-updates mx3 project-nav__link--updates tabbed-nav__link type-14"]//span//text()')

		item = KickstarterProjectItem()

		item['project_url'] = response.url[:-9]

		for each_comment_count in comments_count:
			item['comment_num'] = each_comment_count.extract()
			# yield item

		for each_update in updates:
			item['update'] = each_update.extract()

		item['comment'] = []
		for each_comment in comments:
			# item = KickstarterProjectItem()
			item['comment'].append(each_comment.extract())


		yield item

	def load_urls(self):
		urls = []
		with open('urls.txt') as fp:
			for line in fp:
				urls.append(line[:-1])
		return urls;
