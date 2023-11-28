from awskservices.boto3_client import boto3_helpers


class AWSRegion(boto3_helpers):
    def __init__(self, account=None) -> None:
        super().__init__("lightsail", None)

    def get_all_regions(self):
        response = self.client.get_regions(
            includeAvailabilityZones=False,
            includeRelationalDatabaseAvailabilityZones=False
        )
        return response['regions']
