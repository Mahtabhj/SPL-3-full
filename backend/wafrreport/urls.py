from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import ReportJson, ReportPDF

router = DefaultRouter()

urlpatterns = [
    path("json/", ReportJson.as_view(), name="report_json"),
    path("pdf/", ReportPDF.as_view(), name="report_pdf"),

] + router.urls
