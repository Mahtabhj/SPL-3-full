from typing import Any
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from awskservices.reports import WellArchitectedReports

from awskservices.initiate_view import initiate


class ReportJson(APIView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def get(self, request, format=None):
        self.account = initiate(request=request)
        self.wellArchitectedReports = WellArchitectedReports(self.account)
        query_params = request.query_params
        workloadId = query_params.get('workloadId')
        lensAlias = query_params.get('lensAlias')
        pillarId = query_params.get('pillarId')
        return Response(self.wellArchitectedReports.generate_json_report(workloadId, lensAlias, pillarId), status=status.HTTP_200_OK)


class ReportPDF(APIView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def get(self, request, format=None):
        self.account = initiate(request=request)
        self.wellArchitectedReports = WellArchitectedReports(self.account)
        query_params = request.query_params
        workloadId = query_params.get('workloadId')
        lensAlias = query_params.get('lensAlias')
        pdf_status = self.wellArchitectedReports.generate_pdf_report(
            workloadId, lensAlias)

        import io as BytesIO
        # import base64
        from django.http import HttpResponse

        buffer = BytesIO.BytesIO()
        # content = base64.b64decode(b64content)
        buffer.write(pdf_status)

        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/pdf",
        )
        response['Content-Disposition'] = 'attachment;filename=some_file.pdf'
        return response
