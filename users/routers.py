from django.urls import path
from rest_framework import routers

from .views import UserViewSet, TokenObtainView


class UserRouter(routers.SimpleRouter):
    routes = [
        routers.Route(
            url=r"^users{trailing_slash}$",
            mapping={"post": "create", "put": "update", "patch": "partial_update"},
            name="user-update",
            detail=True,
            initkwargs={"suffix": "Instance"},
        ),
        routers.Route(
            url=r"^users/change_password{trailing_slash}$",
            mapping={"put": "change_password", "patch": "change_password"},
            name="user-change-password",
            detail=True,
            initkwargs={},
        ),
    ]


router = UserRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("token/", TokenObtainView.as_view(), name="token-obtain"),
]

urlpatterns += router.urls
