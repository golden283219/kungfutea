from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from users import views

schema_view = get_schema_view(
    openapi.Info(title="Kung Fu Tea API", default_version="v1",),
    public=False,
    permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("api/v1/", include("users.routers")),
    path("api/v1/mails/", include("mails.routers")),
    path("api/v1/notifications/", include("notifications.routers")),
    path("api/v1/getinfo/", views.links_and_RCPassword.as_view()),
    path("api/v1/links/", include("links.routers")),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)