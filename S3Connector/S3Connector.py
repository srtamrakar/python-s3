import os
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
import logging
from typing import NoReturn, Optional
from .exceptions import (
    BucketDoesNotExist,
    CreateBucketFailed,
    DeleteBucketFailed,
    UploadFailed,
    DownloadFailed,
    DeleteObjectFailed,
)

logger = logging.getLogger(__name__)


class S3Connector(object):
    """
    Python module to connect to S3, create/delete buckets, upload/download/delete objects.
    """

    default_config = Config(
        connect_timeout=60,
        read_timeout=60,
        max_pool_connections=50,
        retries={"max_attempts": 4},
    )
    aws_default_region = "eu-central-1"

    def __init__(
        self,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_region: str = None,
        config: Config = None,
    ) -> NoReturn:

        self.config = config if config is not None else S3Connector.default_config
        self.__client = None
        self.__resource = None
        self.aws_region = (
            aws_region if aws_region is not None else S3Connector.aws_default_region
        )

        self._create_client(aws_access_key_id, aws_secret_access_key)

    def _create_client(
        self, aws_access_key_id: str = None, aws_secret_access_key: str = None,
    ) -> NoReturn:

        if any(cred is None for cred in [aws_access_key_id, aws_secret_access_key]):
            self.__client = boto3.client("s3", region_name=self.aws_region)
            self.__resource = boto3.resource("s3", region_name=self.aws_region)
        else:
            self.__client = boto3.client(
                "s3",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=self.aws_region,
            )
            self.__resource = boto3.resource(
                "s3",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=self.aws_region,
            )
        logger.info("S3 client created")

    def exists_bucket(self, bucket: str) -> bool:
        try:
            self.__client.head_bucket(Bucket=bucket)
            return True
        except ClientError:
            return False

    def create_bucket(self, bucket: str) -> NoReturn:
        if self.exists_bucket(bucket):
            logger.warning(f"A bucket with name '{bucket}' already exists.")
            return

        try:
            self.__client.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={"LocationConstraint": self.aws_region},
            )
            logger.info(f"Bucket created: '{bucket}'")
        except Exception:
            raise CreateBucketFailed(bucket=bucket)

    def delete_bucket(self, bucket: str) -> NoReturn:
        try:
            self.__client.delete_bucket(Bucket=bucket)
            logger.info(f"Bucket deleted: '{bucket}'")
        except Exception:
            raise DeleteBucketFailed(bucket=bucket)

    def upload_file(
        self, file_path: str, bucket: str, object_key: str = None
    ) -> NoReturn:
        if object_key is None:
            object_key = os.path.basename(file_path)

        if self.exists_bucket(bucket) is False:
            raise BucketDoesNotExist(bucket=bucket)

        try:
            self.__client.upload_file(file_path, bucket, object_key)
            logger.info(f"Object created: '{bucket}/{object_key}'")
        except Exception:
            raise UploadFailed(
                file_path=file_path, bucket=bucket, object_key=object_key
            )

    def download_file(self, bucket: str, object_key: str, file_path: str) -> NoReturn:
        try:
            self.__resource.Object(bucket, object_key).download_file(file_path)
            logger.info(f"File downloaded: '{file_path}'")
        except Exception:
            raise DownloadFailed(
                bucket=bucket, object_key=object_key, file_path=file_path
            )

    def delete_object(self, bucket: str, object_key: str) -> NoReturn:
        try:
            self.__client.delete_object(Bucket=bucket, Key=object_key)
            logger.info(f"Object deleted: '{bucket}/{object_key}'")
        except Exception:
            raise DeleteObjectFailed(bucket=bucket, object_key=object_key)

    def get_bucket_list(self) -> list:
        resp = self.__client.list_buckets()
        bucket_list = [bucket for bucket in resp["Buckets"]]
        return bucket_list

    def get_object_list(self, bucket: str) -> Optional[list]:
        resp = self.__client.list_objects(Bucket=bucket)
        try:
            return resp["Contents"]
        except KeyError:
            logger.error(f"Failed to get list of object from bucket: '{bucket}'")
            return None

    def get_object_key_list(self, bucket: str):
        return list(
            map(self.get_object_key, self.__resource.Bucket(bucket).objects.all())
        )

    @staticmethod
    def get_object_key(object_summary):
        return object_summary.key
