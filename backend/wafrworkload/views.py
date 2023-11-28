from typing import Any
from rest_framework.views import APIView
from rest_framework.response import Response
from awskservices.workloads import Workloads as WorkloadsAwsService
from rest_framework import status
from rest_framework import permissions
import copy
from awskservices.initiate_view import initiate


class Workloads(APIView):
    permission_classes = [permissions.IsAuthenticated]
    accout = None
    workloadsAwsService = None

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def get(self, request, format=None):
        self.account = initiate(request=request)
        self.workloadsAwsService = WorkloadsAwsService(self.account)
        return Response(self.workloadsAwsService.get_all_workloads(), status=status.HTTP_200_OK)

    def post(self, request, format=None):
        self.account = initiate(request=request)
        self.workloadsAwsService = WorkloadsAwsService(self.account)

        data = {}
        data['workloadName'] = request.data['workloadName']
        data['description'] = request.data['description']
        data['environment'] = request.data['environment']
        data['lenses1'] = copy.deepcopy(request.data['lenses'])
        data['reviewOwner'] = request.user.email
        data['awsRegions'] = request.data['awsRegions']
        return Response(self.workloadsAwsService.create_workload(data), status=status.HTTP_200_OK)

    def put(self, request, format=None):
        self.account = initiate(request=request)
        self.workloadsAwsService = WorkloadsAwsService(self.account)

        data = {}
        data['workloadId'] = request.data['workloadId']
        data['workloadName'] = request.data['workloadName']
        data['description'] = request.data['description']
        data['environment'] = request.data['environment']
        data['reviewOwner'] = request.user.email
        data['awsRegions'] = request.data['awsRegions']

        return Response(self.workloadsAwsService.update_workload(data), status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        self.account = initiate(request=request)
        self.workloadsAwsService = WorkloadsAwsService(self.account)

        query_params = request.query_params
        workloadId = query_params.get('workloadId')

        return Response(self.workloadsAwsService.delete_workload(workloadId=workloadId), status=status.HTTP_200_OK)


class ViewWorkload(APIView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.workloads = WorkloadsAwsService()

    def get(self, request, format=None):
        self.account = initiate(request=request)
        self.workloadsAwsService = WorkloadsAwsService(self.account)
        query_params = request.query_params
        workloadId = query_params.get('workloadId')
        return Response(self.workloadsAwsService.get_workload(workloadId=workloadId), status=status.HTTP_200_OK)
