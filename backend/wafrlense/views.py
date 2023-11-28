from rest_framework.views import APIView
from rest_framework.response import Response
from awskservices.lense import Lense
from rest_framework import status
from rest_framework import permissions


from awskservices.initiate_view import initiate


class ListLense(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        self.account = initiate(request=request)
        self.lense = Lense(self.account)
        return Response(self.lense.get_all_lense(), status=status.HTTP_200_OK)
