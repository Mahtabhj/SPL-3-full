import boto3


class boto3_helpers():
    def __init__(self, service="wellarchitected", account=None) -> None:
        if account is None:
            self.client = boto3.client(service)
        else:
            role_arn = account.arn_of_iam_role
            external_id = account.external_id
            temp_client = boto3.client('sts')

            response = temp_client.assume_role(
                RoleArn=role_arn,
                RoleSessionName='AssumeRoleSession',
                ExternalId=external_id
            )
            credentials = response['Credentials']
            self.client = boto3.client(service,
                                       aws_access_key_id=credentials['AccessKeyId'],
                                       aws_secret_access_key=credentials['SecretAccessKey'],
                                       aws_session_token=credentials['SessionToken']
                                       )
