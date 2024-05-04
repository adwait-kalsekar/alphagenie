from django.urls import path, include

from . import views

urlpatterns = [
    path("view-bots", views.viewBots, name="viewBots"),
    path("create-bot/", views.createBot, name="createBot"),
    path("delete-bot/<str:id>/", views.deleteBot, name="deleteBot"),
    path("change-bot-status/<str:id>", views.change_bot_status, name="changeStatus"),
    path("bot-details/<str:id>/", views.botDetails, name="botDetails"),
    path("view-buckets/", views.viewBuckets, name="viewBuckets"),
    path("create-bucket/", views.createBucket, name="createBucket"),
    path("delete-bucket/<str:id>/", views.deleteBucket, name="deleteBucket"),
    path("bucket-details/<str:id>/", views.bucketDetails, name="bucketDetails"),
    
    path("confirmDelete/<str:resource>/<str:id>/", views.confirmDelete, name="confirmDelete"),

    # render 404 error page
    path("<path:all_path>/", views.pageNotFoundError),
]
