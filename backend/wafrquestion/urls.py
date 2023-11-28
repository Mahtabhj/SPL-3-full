from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import Questions, Answer

router = DefaultRouter()

urlpatterns = [
    path("", Questions.as_view(), name="all_questions"),
    path("answer/", Answer.as_view(), name="answer_question")
] + router.urls
