from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("categories", views.categories, name="categories"),
    path("mylistings", views.mylistings, name="mylistings"),
    path("closed", views.closed, name="closed"),
    path("categories/<str:category_param>", views.category_get, name="category_get"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("item/<int:item_id>", views.item, name="item"),
    path("comment/<int:item_id>", views.comment, name="comment"),
    path("create", views.create, name="create"),
    path("register", views.register, name="register")
]
