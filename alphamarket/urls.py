from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="dashboard"),
    path("markets/", views.markets, name="markets"),
    path("market-details/<str:ticker>", views.market_details, name="market_details"),

    # render 404 error page
    path("<path:all_path>/", views.errorPage, name="error"),
]
