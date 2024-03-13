from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("trader/", include("alphatrader.urls")),
    path("dashboard/", include("alphamarket.urls")),
    path("", include("alphahome.urls")),
]
