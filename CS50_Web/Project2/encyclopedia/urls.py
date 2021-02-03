from django.urls import path

from . import views

urlpatterns = [
    # Home Page
    path("", views.index, name="index"),
    # @TODO: why switching the order of defining search and entry solve the problem?
    # SearchResult Page
    path("wiki/search_result", views.search, name="search"),
    # Add Page
    path("wiki/createEntry", views.create, name="create"),
    # Random Page
    path("wiki/random", views.random, name="random"),
    # Entry Page
    path("wiki/<str:title>", views.entry, name="entry"),
]
