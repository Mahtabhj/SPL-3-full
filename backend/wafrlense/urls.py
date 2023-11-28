from rest_framework.routers import DefaultRouter
from .views import ListLense
from django.urls import path
router = DefaultRouter()


urlpatterns = [
    path("", ListLense.as_view(), name="all_lense")
] + router.urls
