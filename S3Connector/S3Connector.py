import os
import boto3
import botocore
import logging
from typing import NoReturn, Optional

logger = logging.getLogger(__name__)


class S3Connector(object):
    """
    Python module to connect to S3, create/delete buckets, upload/download/delete objects.
    """

    def __init__(
        self,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_region_name: str = None,
    ) -> NoReturn:
        self._create_client(aws_access_key_id, aws_secret_access_key, aws_region_name)

    def _create_client(
        self,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_region_name: str = None,
    ) -> NoReturn:

        self._aws_region_name = aws_region_name

        if any(
            cred is None
            for cred in [aws_access_key_id, aws_secret_access_key, aws_region_name]
        ):
            self.client = boto3.client("s3")
            self.resource = boto3.resource("s3")
        else:
            self.client = boto3.client(
                "s3",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=aws_region_name,
            )
            self.resource = boto3.resource(
                "s3",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=aws_region_name,
            )

        logger.info("S3 client created")

    def exists_bucket(self, bucket_name: str) -> bool:
        try:
            self.client.head_bucket(Bucket=bucket_name)
            return True
        except botocore.exceptions.ClientError as err:
            return False

    def create_bucket(self, bucket_name: str) -> NoReturn:
        if self.exists_bucket(bucket_name):
            logger.warning(
                "Cannot create the bucket. "
                + f"A bucket with the name '{bucket_name}' already exists."
            )
            return

        try:
            self.client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": self._aws_region_name},
            )
            logger.info(f"Bucket created: {bucket_name}")
        except Exception as err:
            logger.error(f"Failed to create bucket: {bucket_name}")
            raise Exception

    def delete_bucket(self, bucket_name: str) -> NoReturn:
        try:
            self.client.delete_bucket(Bucket=bucket_name)
            logger.info(f"Bucket deleted: {bucket_name}")
        except Exception as err:
            logger.error(f"Failed to delete bucket: {bucket_name}")
            raise Exception

    def upload_file(
        self, file_path: str, bucket_name: str, object_name: str = None
    ) -> NoReturn:
        # If S3 object_name was not specified, use basename of file_path
        if object_name is None:
            object_name = os.path.basename(file_path)

        if self.exists_bucket(bucket_name) is False:
            logger.warning(f"Bucket does not exist: {bucket_name}")
            return

        try:
            self.client.upload_file(file_path, bucket_name, object_name)
            logger.info(f"File uploaded: {bucket_name}/{object_name}")
        except Exception as err:
            logger.error(f"Failed to upload file: {file_path}")
            raise Exception

    def download_file(
        self, bucket_name: str, object_name: str, file_path: str
    ) -> NoReturn:
        try:
            self.resource.Object(bucket_name, object_name).download_file(file_path)
            logger.info(f"Object downloaded: {file_path}")
        except Exception as err:
            logger.error(f"Failed to download object: {bucket_name}/{object_name}")
            raise Exception

    def delete_object(self, bucket_name: str, object_name: str) -> NoReturn:
        try:
            self.client.delete_object(Bucket=bucket_name, Key=object_name)
            logger.info(f"Object deleted: {bucket_name}/{object_name}")
        except Exception as err:
            logger.error(f"Failed to delete object: {bucket_name}/{object_name}")
            raise Exception

    def get_list_of_buckets(self) -> list:
        resp = self.client.list_buckets()
        bucket_list = [bucket for bucket in resp["Buckets"]]
        return bucket_list

    def get_list_of_objects(self, bucket_name: str) -> Optional[list]:
        resp = self.client.list_objects(Bucket=bucket_name)
        try:
            return resp["Contents"]
        except KeyError as err:
            logger.error(f"Failed to get list of object: {bucket_name}")
            return None

    def get_list_of_all_object_keys(self, bucket_name: str):
        return list(
            map(self.get_object_key, self.resource.Bucket(bucket_name).objects.all())
        )

    @staticmethod
    def get_object_key(object_summary):
        return object_summary.key
