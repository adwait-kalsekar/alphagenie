from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="dashboard"),
    path("markets/", views.markets, name="markets"),
    path("market-details/<str:ticker>", views.marketDetails, name="marketDetails"),
    path("predictions/", views.predictions, name="predictions"),
    path("predictions-details/<str:ticker>", views.predictionDetails, name="predictionDetails"),

    # render 404 error page
    path("<path:all_path>/", views.pageNotFoundError),
]
