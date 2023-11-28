from django.urls import path
from rest_framework.routers import DefaultRouter
from wafrcloudaccount.views.add_aws_accounts import AwsAccountViewSet
from wafrcloudaccount.views.get_billing_accounts import GetBillingDataAPIView
from wafrcloudaccount.views.get_last_added_aws_account import GetLastAddedAWSAccountApiView
from wafrcloudaccount.views.get_own_accounts import GetAwsAccountListAPIView
from wafrcloudaccount.views.get_account import GetAccountView
router = DefaultRouter()
router.register(r'aws-accounts', AwsAccountViewSet)

urlpatterns = [
    path('get-billing-data/', GetBillingDataAPIView.as_view()),
    path('get-last-added-aws-account/', GetLastAddedAWSAccountApiView.as_view()),
    path('get-aws-account-list/', GetAwsAccountListAPIView.as_view()),
    path('get-account/', GetAccountView.as_view())
] + router.urls
