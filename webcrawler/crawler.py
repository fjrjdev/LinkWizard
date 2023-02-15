from scrapy.spiders import Rule, Spider
import scrapy
from urllib.parse import urljoin


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
