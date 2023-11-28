import logging
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ..models import AwsAccount
from ..services.billing_data_services import BillingDataService

logger = logging.getLogger(__name__)


class GetAwsAccountListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):

        try:
            account_qs = AwsAccount.objects.filter(created_by=request.user.id)
            response = []
            for account in account_qs:
                response.append({
                    "id": account.id,
                    "account_id": account.name,
                    "arn_of_iam_role": account.arn_of_iam_role,
                    "bucket_name": account.bucket_name,
                    "report_name": account.report_name,
                    "prefix_path": account.prefix_path,
                    "external_id": account.external_id,
                })
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Server Error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
