from django.urls import path
from user.views import CreateUserView, LoginUserView, ManageUserView
from rest_framework.authtoken import views

app_name = "user"
urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register_user"),
    path("login/", LoginUserView.as_view(), name="get_auth_token"),
    path("me/", ManageUserView.as_view(), name="manage.user")
]
