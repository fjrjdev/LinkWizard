from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Rule, Spider
from scrapy.linkextractors import LinkExtractor
import scrapy
from urllib.parse import urljoin
from scrapy.signalmanager import dispatcher
from scrapy import signals

import subprocess


class DevgoSpider(Spider):
    name = "devgo_spider"

    allowed_domains = ["devgo.com.br"]
    start_urls = ["https://devgo.com.br/"]

    def __init__(self, *args, **kwargs):
        super(DevgoSpider, self).__init__(*args, **kwargs)
        self.visited_urls = set()

    @staticmethod
    def is_valid_url(url):
        if not url.startswith("http"):
            return False
        exclude = ["discord.gg", "hashnode.com"]
        for e in exclude:
            if e in url:
                return False
        if url is None:
            return False
        return True

    def parse(self, response):
        links = response.xpath("//a")
        for link in links:
            url = link.xpath("@href").get()
            label = link.xpath("text()").get()

            if not url:
                continue

            url = response.urljoin(url)

            if label is None:
                continue

            if not self.is_valid_url(url):
                continue

            if url in self.visited_urls:
                continue

            self.visited_urls.add(url)

            yield {"url": url, "label": label}


def iniciar_crawler(nome_do_spider):
    #     # chama o comando scrapy crawl nome_do_spider no terminal
    subprocess.run(["scrapy", "runspider", nome_do_spider])


# def spider_results():
#     results = []

#     def crawler_results(signal, sender, item, response, spider):
#         results.append(item)

#     dispatcher.connect(crawler_results, signal=signals.item_scraped)

#     process = CrawlerProcess()
#     process.crawl(DevgoSpider)
#     process.start()
#     return results


# process.start()
