from rest_framework.views import APIView, Request, Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

import requests
from bs4 import BeautifulSoup

from .serializers import CrawledDataSerializer
from links.models import Link
from links.permissions import IsAdminOwnerLink
import uuid


class CrawlerView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOwnerLink, IsAuthenticated]

    def get(self, request):
        data = crawler()

        links_created = []
        for link in data:
            obj, created = Link.objects.get_or_create(
                url=link.get("url"),
                defaults={
                    "id": uuid.uuid4(),
                    "url": link.get("url"),
                    "label": link.get("label"),
                    "user": self.request.user,
                },
            )
            if created:
                links_created.append(obj)

        if links_created:
            serializer = CrawledDataSerializer(links_created, many=True)
            return Response(serializer.data)

        return Response({"detail": "Links já foram coletados anteriormente"})


def crawler(url="https://devgo.com.br"):
    response = requests.get(url)
    url_list = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        h1_tags = soup.find_all("h1")
        for h1_tag in h1_tags:
            a_tag = h1_tag.find("a")
            href = a_tag["href"]
            text = a_tag.text
            if href and href.startswith("/"):
                href = url + href
            if href != url + "/":
                url_list.append({"url": href, "label": text})

    return url_list
