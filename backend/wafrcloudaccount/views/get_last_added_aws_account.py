import boto3
import logging
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ..models import AwsAccount
from ..services.billing_data_services import BillingDataService

logger = logging.getLogger(__name__)

class GetLastAddedAWSAccountApiView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):

        try:
            account = AwsAccount.objects.filter(created_by=request.user.id).last()
            response = dict()
            if account:
                response.update({"account_id": account.name,
                                 "arn_of_iam_role": account.arn_of_iam_role,
                                 "bucket_name": account.bucket_name,
                                 "report_name": account.report_name,
                                 "external_id": account.external_id,
                                 "prefix_path": account.prefix_path,
                                 })
            else:
                return Response({
                    'message': 'No account found with this user.'
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Server Error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
