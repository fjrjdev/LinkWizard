from django.urls import path
from . import views

urlpatterns = [
    path("links/", views.LinkView.as_view()),
    path("links/<pk>/", views.LinkDetailView.as_view()),
]
