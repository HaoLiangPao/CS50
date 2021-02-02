from django.urls import path

from . import views

urlpatterns = [
    # Home Page
    path("", views.index, name="index"),
    # Entry Page
    path("wiki/<str:title>", views.entry, name="entry"),
    # SearchResult Page
    path("wiki/search_result", views.search, name="search")
    # Add Page

]
