from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from wafrauth.views.views import UserViewSet, MyTokenObtainPairView
from wafrauth.views.register_user_api_view import RegisterUserAPIView, VerifyOTP
from wafrauth.views.change_password_view import ChangePasswordView
from wafrauth.views.password_reset_view import SendPasswordResetCodeApiView, PasswordResetApiView
from wafrauth.views.profile_picture_view import UserProfileView

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterUserAPIView.as_view()),
    path('verify/', VerifyOTP.as_view()),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('send-password-reset-code/', SendPasswordResetCodeApiView.as_view(),
         name='send_password_reset_code'),
    path('password-reset/', PasswordResetApiView.as_view(),
         name='password_reset'),
    path('user-profile/', UserProfileView.as_view(), name='user_profile')
] + router.urls
