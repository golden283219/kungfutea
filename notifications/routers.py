from rest_framework.routers import SimpleRouter

from notifications.views import NotificationViewSet
# setting router
router = SimpleRouter()
router.register("", NotificationViewSet, basename="notification")

urlpatterns = router.urls
