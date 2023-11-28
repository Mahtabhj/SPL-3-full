from awskservices.boto3_client import boto3_helpers


class Lense(boto3_helpers):
    def __init__(self, account=None) -> None:
        self.lense_records = []
        super().__init__(account=account)

    def get_all_lense(self, lenstype='', lensStatus='PUBLISHED', maxResults=50):
        nextToken = ""
        while True:
            response = self.client.list_lenses(
                NextToken=nextToken,
                MaxResults=maxResults,
                LensType=lenstype,
                LensStatus=lensStatus,
                # LensName=lensName
            )
            self.lense_records = self.lense_records + \
                response['LensSummaries']
            if 'NextToken' in response:
                nextToken = response['NextToken']
                if not nextToken or nextToken == "":
                    break
            else:
                break

        return self.lense_records
