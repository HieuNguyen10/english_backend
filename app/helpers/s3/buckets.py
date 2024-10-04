from enum import Enum
import boto3
from botocore.client import BaseClient
from fastapi import Depends
from app.helpers.config import settings
import boto3.session
session = boto3.session.Session(region_name='ap-southeast-1')

def s3_auth() -> BaseClient:
    s3 = boto3.client(service_name='s3', aws_access_key_id=settings.AWS_SERVER_PUBLIC_KEY,
                      aws_secret_access_key=settings.AWS_SERVER_SECRET_KEY,
                      config= boto3.session.Config(signature_version='s3v4')
                      )

    return s3

def get_list_of_buckets(s3: BaseClient = Depends(s3_auth)):
    response = s3.list_buckets()
    buckets = {}

    for buckets in response['Buckets']:
        buckets[response['Name']] = response['Name']

    BucketName = Enum('BucketName', buckets)

    return BucketName