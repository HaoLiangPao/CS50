from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("watchList", views.watchList, name="watchList"),
    path("create", views.create, name="create"),
    path("listing/<str:id>", views.listing, name="listing"),

]



