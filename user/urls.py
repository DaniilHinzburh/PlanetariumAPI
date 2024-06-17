from django.urls import path
from user.views import CreateUserViewSet

app_name = "user"
urlpatterns = [
    path("register/", CreateUserViewSet.as_view(), name="register_user", )
]
