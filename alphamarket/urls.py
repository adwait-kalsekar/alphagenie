from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="dashboard"),
    path("markets/", views.markets, name="markets"),

    # render 404 error page
    path("<path:all_path>/", views.errorPage, name="error"),
]
