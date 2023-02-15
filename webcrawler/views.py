from rest_framework.views import APIView, Request, Response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

import uuid
import django

from .crawler import DevgoSpider, iniciar_crawler

from links.models import Link
from links.permissions import IsAdminOwnerLink
from links.serializers import LinkSerializer

from concurrent.futures import ProcessPoolExecutor
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy import signals
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
import multiprocessing


def run_spider(spider):
    items = []

    def item_scraped(item, response, spider):
        items.append(item)

    configure_logging()
    process = CrawlerProcess()
    crawler = process.create_crawler(spider)
    crawler.signals.connect(item_scraped, signal=signals.item_scraped)
    process.crawl(crawler)
    process.start()
    return items


user = None


class CrawlerView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        global user
        user = self.request.user
        with ProcessPoolExecutor(
            max_workers=4,
            mp_context=multiprocessing.get_context("spawn"),
            initializer=django.setup,
        ) as executor:
            future1 = executor.submit(run_spider, DevgoSpider)
            future1.add_done_callback(process_data)
        return Response(status=status.HTTP_202_ACCEPTED)


def process_data(future):
    global user
    try:
        data = future.result()

        for link in data:
            obj, created = Link.objects.get_or_create(
                url=link.get("url"),
                user=user,
                defaults={
                    "id": uuid.uuid4(),
                    "url": link.get("url"),
                    "label": link.get("label"),
                    "user": user,
                },
            )

    except Exception as e:
        print(e)
