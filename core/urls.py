from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("dashboard/alphabots/", include("alphabots.urls")),
    path("dashboard/trader/", include("alphatrader.urls")),
    path("dashboard/", include("alphamarket.urls")),
    path("", include("alphahome.urls")),
]
