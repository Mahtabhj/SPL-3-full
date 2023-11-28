from awskservices.boto3_client import boto3_helpers


class Workloads(boto3_helpers):
    def __init__(self, account=None) -> None:
        super().__init__(account=account)
        self.workload_records = []

    def get_all_workloads(self, workloadNamePrefix='', maxResults=50):
        nextToken = ""
        while True:
            response = self.client.list_workloads(
                WorkloadNamePrefix=workloadNamePrefix,
                NextToken=nextToken,
                MaxResults=maxResults
            )
            self.workload_records = self.workload_records + \
                response['WorkloadSummaries']
            if 'NextToken' in response:
                nextToken = response['NextToken']
                if not nextToken or nextToken == "":
                    break
            else:
                break

        return self.workload_records

    def get_workload(self, workloadId):
        response = self.client.get_workload(
            WorkloadId=workloadId
        )
        return response['Workload']

    def create_workload(self, data):
        response = self.client.create_workload(
            WorkloadName=data['workloadName'],
            Description=data['description'],
            Environment=data['environment'],
            Lenses=data['lenses1'],
            ReviewOwner=data['reviewOwner'],
            AwsRegions=data['awsRegions']

        )
        return self.get_workload(response['WorkloadId'])

    def update_workload(self, data):
        response = self.client.update_workload(
            WorkloadId=data['workloadId'],
            WorkloadName=data['workloadName'],
            Description=data['description'],
            Environment=data['environment'],
            ReviewOwner=data['reviewOwner'],
            AwsRegions=data['awsRegions']

        )
        return response['Workload']

    def delete_workload(self, workloadId):
        try:
            _ = self.client.delete_workload(
                WorkloadId=workloadId,
            )
            return {
                "Message": f"{workloadId} Deleted"
            }
        except Exception as e:
            return {
                "Message": "Something went to wrong. Please Check workload id",
                "Error": str(e)
            }
