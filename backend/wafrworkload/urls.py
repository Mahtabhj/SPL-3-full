from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import Workloads, ViewWorkload

router = DefaultRouter()

urlpatterns = [
    path("", Workloads.as_view(), name="all_workloads"),
    path("view/", ViewWorkload.as_view(), name="view_workloads")
] + router.urls
