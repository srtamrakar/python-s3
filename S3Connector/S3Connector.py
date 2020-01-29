import io
import os
import re
import sys
import boto3
import botocore
import logging
import traceback
import pandas as pd
from typing import NoReturn

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


logger = logging.getLogger(__name__)


class S3Connector(object):
    """
    Python module to connect to S3, create/delete buckets, upload/download/delete objects.
    """

    # general csv features
    _csv_sep = ","
    _csv_null_identifier = "#N/A"

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

        if aws_region is None:
            aws_region = "eu-central-1"

        self._aws_access_key_id = aws_access_key_id
        self._aws_secret_access_key = aws_secret_access_key
        self._aws_region = aws_region

        if None not in [
            self._aws_access_key_id,
            self._aws_secret_access_key,
            self._aws_region,
        ]:
            self._s3_client = boto3.client(
                "s3",
                aws_access_key_id=self._aws_access_key_id,
                aws_secret_access_key=self._aws_secret_access_key,
                region_name=self._aws_region,
            )
            self._s3_resource = boto3.resource(
                "s3",
                aws_access_key_id=self._aws_access_key_id,
                aws_secret_access_key=self._aws_secret_access_key,
                region_name=self._aws_region,
            )
        self._s3_client = boto3.client("s3")
        self._s3_resource = boto3.resource("s3")
        logger.info("S3 client created")

    def _get_list_of_buckets(self) -> list:
        resp = self._s3_client.list_buckets()
        bucket_list = [bucket for bucket in resp["Buckets"]]
        return bucket_list

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
            logger.info(f"Bucket deleted: {bucket_name}/{object_name}")
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
            self._create_bucket(bucket_name)

        # Upload the file
        try:
            self._s3_client.upload_file(file_path, bucket_name, object_name)
            logger.info(f"File uploaded: {bucket_name}/{object_name}")
            return True
        except botocore.exceptions.ClientError as err:
            logger.error(err)
            logger.error(traceback.format_exc())
            return False

    def upload_dataframe_as_csv(
        self,
        dataframe: pd.DataFrame = None,
        bucket_name: str = None,
        object_name: str = None,
        csv_sep: str = None,
        csv_null_identifier: str = None,
    ) -> bool:
        if None in [dataframe, bucket_name, object_name]:
            logger.warning("Dataframe / Bucket name / Object name is not specified")
            return False
        if csv_sep is None:
            csv_sep = self._csv_sep
        if csv_null_identifier is None:
            csv_null_identifier = self._csv_null_identifier

        try:
            # save dataframe as temp csv
            csv_io = io.StringIO()
            dataframe.to_csv(
                csv_io,
                sep=csv_sep,
                encoding="utf-8-sig",
                header=True,
                index=False,
                na_rep=csv_null_identifier,
            )
            csv_contents = csv_io.getvalue()
            csv_contents = re.sub(r"NaT", csv_null_identifier, csv_contents)
            csv_io.seek(0)
            csv_io.write(csv_contents)

            # copy temp csv file to S3 object
            if self._exists_bucket(bucket_name) is False:
                self._create_bucket(bucket_name)
            self._s3_resource.Object(bucket_name, object_name).put(
                Body=csv_io.getvalue()
            )
            csv_io.close()

            logger.info(f"File uploaded: {bucket_name}/{object_name}")
            return True
        except Exception as err:
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

    def _get_s3_object_path(
        self, bucket_name: str = None, object_name: str = None
    ) -> str:
        return "s3://{0}/{1}".format(bucket_name, object_name)
