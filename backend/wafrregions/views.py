from typing import Any
from rest_framework.views import APIView
from rest_framework.response import Response
from awskservices.regions import AWSRegion
from rest_framework import status
from rest_framework import permissions

from awskservices.initiate_view import initiate


class ListRegions(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def get(self, request, format=None):
        self.account = initiate(request=request)
        self.regionService = AWSRegion(self.account)
        return Response(self.regionService.get_all_regions(), status=status.HTTP_200_OK)
