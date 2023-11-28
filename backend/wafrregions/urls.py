from rest_framework.routers import DefaultRouter
from .views import ListRegions
from django.urls import path
router = DefaultRouter()


urlpatterns = [
    path("", ListRegions.as_view(), name="all_regions")
] + router.urls
