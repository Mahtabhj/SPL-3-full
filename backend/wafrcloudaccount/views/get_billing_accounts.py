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

class GetBillingDataAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):

        try:
            account_id = request.data.get('account_id', None)
            account = AwsAccount.objects.filter(name=account_id).first()

            if account:
                s3_client = BillingDataService().get_s3_client(account)
                bucket_name = account.bucket_name
            else:
                return Response({
                    'message': 'No account found with this account_id!'
                }, status=status.HTTP_404_NOT_FOUND)

            report_file_obj = BillingDataService().get_last_modified_report_object(
                s3_client, bucket_name)

            response = s3_client.get_object(Bucket=bucket_name, Key=report_file_obj['Key'])
            csv_data = BillingDataService.get_csv_data_by_decompressing_report_file(response)

            # iterate over each column to get needed column name
            billing_period_start_date_column = None
            service_name_column = None
            pricing_column = None
            for idx, row in enumerate(csv_data):
                if idx>0:
                    break
                for col_idx,col in enumerate(row):
                    if col=='bill/BillingPeriodStartDate':
                        billing_period_start_date_column = col_idx
                    if col=='lineItem/ProductCode':
                        service_name_column = col_idx
                    if col=='pricing/publicOnDemandCost':
                        pricing_column = col_idx

            cloud_services_with_cost = dict()
            # iterate over each row of the csv data
            total_cost = 0
            for idx, row in enumerate(csv_data):
                if idx==0:
                    continue
                # billing_period_start_date = datetime.strptime(row[billing_period_start_date_column], "%Y-%m-%dT%H:%M:%SZ")
                # month = str(billing_period_start_date.month)

                ind_cost = float(row[pricing_column]) if row[pricing_column] else 0
                cloud_service_name = str(row[service_name_column])
                total_cost += ind_cost

                if cloud_service_name not in cloud_services_with_cost:
                    cloud_services_with_cost[cloud_service_name] = ind_cost
                    # cloud_services_with_cost[cloud_service_name] = {}
                    # cloud_services_with_cost[cloud_service_name][month] = ind_cost
                else:
                    cloud_services_with_cost[cloud_service_name] += ind_cost
                    # cloud_services_with_cost[cloud_service_name] += "%.6f" % float(cloud_services_with_cost[cloud_service_name])
                    # if month not in cloud_services_with_cost[cloud_service_name]:
                    #     cloud_services_with_cost[cloud_service_name][month] = ind_cost
                    # else:
                    #     cloud_services_with_cost[cloud_service_name][month] += ind_cost

            for key in cloud_services_with_cost:
                cloud_services_with_cost[key] = "%.2f" % cloud_services_with_cost[key]
            now = datetime.now()
            month_name = now.strftime('%B')
            response = {
                "total_cost": "%.2f" %  total_cost,
                "month": month_name,
                "cloud_services_with_cost": cloud_services_with_cost
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Server Error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
