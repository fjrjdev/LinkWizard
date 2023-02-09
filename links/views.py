from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.authentication import TokenAuthentication

from .models import Link
from .serializers import LinkSerializer
from .permissions import IsAdminOrUser


class LinkView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrUser]
    queryset = Link.objects.all()
    serializer_class = LinkSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
