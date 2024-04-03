from django.urls import path, include

from . import views

urlpatterns = [
    path("viewBots", views.viewBots, name="viewBots"),
    path("createBot/", views.createBot, name="createBot"),
    path("viewBuckets/", views.viewBuckets, name="viewBuckets"),
    path("createBucket/", views.createBucket, name="createBucket"),

    # render 404 error page
    path("<path:all_path>/", views.errorPage, name="error"),
]
