import os
import boto3
import botocore
import logging
import traceback
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
        aws_region: str = None,
    ) -> NoReturn:
        self._create_client(aws_access_key_id, aws_secret_access_key, aws_region)

    def _create_client(
        self,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_region: str = None,
    ) -> NoReturn:

        self._aws_region = aws_region

        if None not in [
            aws_access_key_id,
            aws_secret_access_key,
            aws_region,
        ]:
            self._s3_client = boto3.client(
                "s3",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=aws_region,
            )
            self._s3_resource = boto3.resource(
                "s3",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=aws_region,
            )
        else:
            self._s3_client = boto3.client("s3")
            self._s3_resource = boto3.resource("s3")
        logger.info("S3 client created")

    def _exists_bucket(self, bucket_name: str = None) -> bool:
        if bucket_name is None:
            logger.warning("Bucket name is not specified")
            return False

        try:
            self._s3_client.head_bucket(Bucket=bucket_name)
            return True
        except botocore.exceptions.ClientError as err:
            logger.error(err)
            logger.error(traceback.format_exc())
            return False

    def _create_bucket(self, bucket_name: str = None) -> bool:
        if bucket_name is None:
            logger.warning("Bucket name is not specified")
            return False

        if self._exists_bucket(bucket_name):
            logger.warning(
                f"Cannot create the bucket. A bucket with the name '{bucket_name}' already exists."
            )

        try:
            self._s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": self._aws_region},
            )
            logger.info(f"Bucket created: {bucket_name}")
            return True
        except Exception as err:
            logger.error(err)
            logger.error(traceback.format_exc())
            return False

    def _delete_bucket(self, bucket_name: str = None) -> bool:
        if bucket_name is None:
            logger.warning("Bucket name is not specified")
            return False

        try:
            self._s3_client.delete_bucket(Bucket=bucket_name)
            logger.info(f"Bucket deleted: {bucket_name}")
            return True
        except botocore.exceptions.ClientError as err:
            logger.error(err)
            logger.error(traceback.format_exc())
            return False

    def upload_file(self, file_path=None, bucket_name=None, object_name=None) -> bool:
        if bucket_name is None:
            logger.warning("Bucket name is not specified")
            return False

        # If S3 object_name was not specified, use basename of file_path
        if object_name is None:
            object_name = os.path.basename(file_path)

        if self._exists_bucket(bucket_name) is False:
            logger.warning(f"Bucket does not exist: {bucket_name}")
            return False

        # Upload the file
        try:
            self._s3_client.upload_file(file_path, bucket_name, object_name)
            logger.info(f"File uploaded: {bucket_name}/{object_name}")
            return True
        except botocore.exceptions.ClientError as err:
            logger.error(err)
            logger.error(traceback.format_exc())
            return False

    def download_file(
        self, bucket_name: str = None, object_name: str = None, file_path: str = None
    ) -> bool:
        if None in [bucket_name, object_name]:
            logger.warning("Bucket name / Object name is not specified")
            return False

        try:
            self._s3_resource.Object(bucket_name, object_name).download_file(file_path)
            logger.info(f"Object downloaded: {bucket_name}/{object_name}")
            return True
        except Exception as err:
            logger.error(err)
            logger.error(traceback.format_exc())
            return False

    def delete_object(self, bucket_name: str = None, object_name: str = None) -> bool:
        try:
            self._s3_client.delete_object(Bucket=bucket_name, Key=object_name)
            logger.info(f"Object deleted: {bucket_name}/{object_name}")
            return True
        except botocore.exceptions.ClientError as err:
            logger.error(err)
            logger.error(traceback.format_exc())
            return False

    def get_list_of_buckets(self) -> list:
        resp = self._s3_client.list_buckets()
        bucket_list = [bucket for bucket in resp["Buckets"]]
        return bucket_list

    def get_objects(self, bucket_name: str = None) -> Optional[list]:
        if bucket_name is None:
            logger.warning("Bucket name is not specified")
            return None

        resp = self._s3_client.list_objects(Bucket=bucket_name)
        try:
            return resp["Contents"]
        except KeyError as err:
            logger.error(err)
            logger.error(traceback.format_exc())
            return None
