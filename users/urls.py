from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

from . import views

urlpatterns = [
    path("create/", views.CreateUserView.as_view()),
    path("login/", ObtainAuthToken.as_view()),
]
