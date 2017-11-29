from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector
from kickstarter_project.items import KickstarterProjectItem


class MySpider(BaseSpider):
    name = "craig"
    allowed_domains = ["kickstarter.com"]
    start_urls = ["https://www.kickstarter.com/projects/inspero/vinci-20-worlds-first-standalone-ai-sports-headpho/comments"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.xpath("//span[@class='pl']")
        items = []
        for titles in titles:
            item = KickstarterProjectItem()
            item["title"] = titles.select("a/text()").extract()
            item["link"] = titles.select("a/@href").extract()
            items.append(item)
        return items