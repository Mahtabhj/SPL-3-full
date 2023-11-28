from awskservices.boto3_client import boto3_helpers
import base64


class WellArchitectedReports(boto3_helpers):
    def __init__(self, account=None) -> None:
        super().__init__(account=account)

    def generate_json_report(self, workloadId, lensAlias, pillarId):
        response = self.client.get_lens_review(
            WorkloadId=workloadId,
            LensAlias=lensAlias,
        )
        summaries = response['LensReview']['PillarReviewSummaries']
        for summary in summaries:
            print(summary['PillarId'], pillarId)
            if summary['PillarId'] == pillarId:
                return summary
        return "Pillar Not Found"

    def generate_pdf_report(self, workloadId, lensAlias):
        response = self.client.get_lens_review_report(
            WorkloadId=workloadId,
            LensAlias=lensAlias,
        )
        base64_data = response['LensReviewReport']['Base64String']
        pdf_data = base64.b64decode(base64_data)
        return pdf_data
