from rest_framework.views import APIView, Request, Response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

import uuid
import django
import multiprocessing

from links.models import Link

from concurrent.futures import ProcessPoolExecutor
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy import signals
from scrapy.utils.log import configure_logging


from .crawler import DevgoSpider


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
            future = executor.submit(run_spider, DevgoSpider)
            future.add_done_callback(process_data)
        return Response(
            data={
                "message": "Sua solicitação foi recebida com sucesso e está em processo de execução. Por favor, aguarde enquanto processamos seus dados"
            },
            status=status.HTTP_202_ACCEPTED,
        )


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
