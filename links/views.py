from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response, status
from .models import Link
from .serializers import LinkSerializer, LinkDetailSerializer
from .permissions import IsAdminOwnerLink


class LinkView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOwnerLink, IsAuthenticated]
    queryset = Link.objects.all()
    serializer_class = LinkSerializer

    def list(self, request):
        links = self.queryset.filter(user=self.request.user)
        serializer = self.serializer_class(links, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LinkDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOwnerLink]

    queryset = Link.objects.all()
    serializer_class = LinkDetailSerializer
