from django.urls import path
from rest_framework import routers

from .views import MenuLinkViewSet, QuickLinkViewSet


router = routers.SimpleRouter()
router.register(r'menulink', MenuLinkViewSet)
router.register(r'quicklink', QuickLinkViewSet)

urlpatterns = [
]

urlpatterns += router.urls
