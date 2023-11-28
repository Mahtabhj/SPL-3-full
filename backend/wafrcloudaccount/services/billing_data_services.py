import boto3
import gzip
import csv


class BillingDataService:

    @staticmethod
    def get_s3_client(account):
        role_arn = account.arn_of_iam_role
        external_id = account.external_id
        sts_client = boto3.client('sts')

        assumed_role_object = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName='AssumeRoleSession',
            ExternalId=external_id
        )

        credentials = assumed_role_object['Credentials']
        s3_client = boto3.client(
            's3',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )
        return s3_client

    @staticmethod
    def get_last_modified_report_object(s3_client, bucket_name):
        cost_report_file_list = []
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        for obj in response['Contents']:
            key = obj['Key']
            if key.lower().endswith('.csv.gz'):
                cost_report_file_list.append(obj)
        report_file_obj = cost_report_file_list[len(cost_report_file_list) - 1]

        return report_file_obj

    @staticmethod
    def get_csv_data_by_decompressing_report_file(response):
        compressed_data = response['Body'].read()
        # decompress the contents of the file
        decompressed_data = gzip.decompress(compressed_data)
        # parse the csv data
        csv_data = csv.reader(decompressed_data.decode('utf-8').splitlines())

        return csv_data
