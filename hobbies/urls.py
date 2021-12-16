from django.urls import path

from .api import (
    accept_friend_request_api,
    auth_check_api,
    auth_login_api,
    auth_logout_api,
    hobbies_api,
    send_friend_request_api,
    users_api,
    user_api,
    user_hobbies_api,
    user_similar_hobbies_api,
)
from .views import register, login, profile, similar

urlpatterns = [
    path("api/auth/check/", auth_check_api, name="auth check api"),
    path("api/auth/login/", auth_login_api, name="auth login api"),
    path("api/auth/logout/", auth_logout_api, name="auth logout api"),
    path("api/hobbies/", hobbies_api, name="hobbies api"),
    path("api/users/", users_api, name="users api"),
    path("api/users/<int:user_id>/", user_api, name="user api"),
    path("api/users/<int:user_id>/hobbies", user_hobbies_api, name="user hobbies api"),
    path(
        "api/users/<int:user_id>/hobbies/similar",
        user_similar_hobbies_api,
        name="user similar hobbies api",
    ),
    path(
        "api/friend_request/send",
        send_friend_request_api,
        name="send friend request api",
    ),
    path(
        "api/friend_request/accept",
        accept_friend_request_api,
        name="accept friend request api",
    ),
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("profile/", profile, name="profile"),
    path("similar/", similar, name="similar"),
]
