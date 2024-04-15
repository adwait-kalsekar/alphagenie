from django.urls import path, include

from . import views

urlpatterns = [
    path("view-bots", views.viewBots, name="viewBots"),
    path("create-bot/", views.createBot, name="createBot"),
    path("view-buckets/", views.viewBuckets, name="viewBuckets"),
    path("create-bucket/", views.createBucket, name="createBucket"),
    path("delete-bucket/<str:id>/", views.deleteBucket, name="deleteBucket"),
    path("bucket-details/<str:id>/", views.bucketDetails, name="bucketDetails"),
    
    path("confirmDelete/<str:resource>/<str:id>/", views.confirmDeleteBucket, name="confirmDeleteBucket"),

    # render 404 error page
    path("<path:all_path>/", views.pageNotFoundError, name="error"),
]
