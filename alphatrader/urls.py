from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.loginUser, name="login"),
    path("signup/", views.signupUser, name="signup"),
    path("logout/", views.logoutUser, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("update-profile/", views.updateProfile, name="update-profile"),
    path("update-password/", views.updatePassword, name="update-password"),
    path("wallet/", views.wallet, name="wallet"),

    # render 404 error page
    path("<path:all_path>/", views.pageNotFoundError, name="error"),
]
