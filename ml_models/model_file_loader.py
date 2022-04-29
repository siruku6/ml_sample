import os
import boto3


def load(bucket: str, source_filepath: str, target_filepath: str):
    client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    )
    client.download_file(bucket, source_filepath, target_filepath)
