from django.urls import path
from . import views

urlpatterns = [path("link/", views.LinkView.as_view())]
