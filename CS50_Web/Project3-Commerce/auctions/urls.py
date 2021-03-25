from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("watchList", views.watchList, name="watchList"),
    path("create", views.create, name="create"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("listing/<int:id>/<str:message>", views.listing, name="listing_message"),
    path("listing/<int:id>/<str:message>/<int:owner>", views.listing, name="listing_owner"),
]



