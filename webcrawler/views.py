from rest_framework.views import APIView, Request, Response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

import uuid

from .crawler import crawler

from links.models import Link
from links.permissions import IsAdminOwnerLink
from links.serializers import LinkSerializer


class CrawlerView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        data = crawler()
        links_created = []
        for link in data:
            obj, created = Link.objects.get_or_create(
                url=link.get("url"),
                user=self.request.user,
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
            serializer = LinkSerializer(links_created, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(
            data={"detail": "Links já foram coletados anteriormente"},
            status=status.HTTP_200_OK,
        )
