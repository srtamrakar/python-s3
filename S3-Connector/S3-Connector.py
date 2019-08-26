import os
import sys

import boto3
import botocore

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class S3(object):

	def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, aws_region_name=None):
		self._create_clients(aws_access_key_id, aws_secret_access_key, aws_region_name)

	def _create_clients(self, aws_access_key_id=None, aws_secret_access_key=None, aws_region_name=None):

		if None not in [aws_access_key_id, aws_secret_access_key, aws_region_name]:
			self._s3_client = boto3.client(
				's3',
				aws_access_key_id=aws_access_key_id,
				aws_secret_access_key=aws_secret_access_key,
				region_name=aws_region_name,
			)
			self._s3_resource = boto3.resource(
				's3',
				aws_access_key_id=aws_access_key_id,
				aws_secret_access_key=aws_secret_access_key,
				region_name=aws_region_name,
			)
		self._s3_client = boto3.client('s3')
		self._s3_resource = boto3.resource('s3')
		return

	def _get_list_of_buckets(self):
		resp = self._s3_client.list_buckets()
		bucket_list = [bucket for bucket in resp['Buckets']]
		return bucket_list

	def _exists_bucket(self, bucket_name=None):
		"""
		Determine whether bucket_name exists and the user has permission to access it
		:param bucket_name: string
		:return: True if the referenced bucket_name exists, otherwise False
		"""
		try:
			resp = self._s3_client.head_bucket(Bucket=bucket_name)
		except botocore.exceptions.ClientError as e:
			print(e)
			return False
		return True

	def _create_bucket(self, bucket_name=None):
		if self._exists_bucket(bucket_name):
			print("Cannot create the bucket. A bucket with the name '" +
				  bucket_name + "' already exists. Exiting.")

		try:
			print("Creating a new bucket named '" + bucket_name + "'...")
			self._s3_client.create_bucket(
				Bucket=bucket_name,
				CreateBucketConfiguration={'LocationConstraint': self._aws_region}
			)
			print("Bucket created")
		except Exception as e:
			print(e)
			sys.exit()
		return

	def _delete_bucket(self, bucket_name):
		print("Deleting the bucket named '" + bucket_name + "'...")
		self._s3_client.delete_bucket(Bucket=bucket_name)
		print("Bucket deleted")

	def upload_file(self, file_path=None, bucket_name=None, object_name=None):
		"""
		Upload a file to an S3 bucket
		:param file_path: File to upload
		:param bucket_name: Bucket to upload to
		:param object_name: S3 object name. If not specified then basename of file path
		:return: True if file was uploaded, else False
		"""
		# If S3 object_name was not specified, use basename of file_path
		if object_name is None:
			object_name = os.path.basename(file_path)

		if not self._exists_bucket(bucket_name):
			self._create_bucket(bucket_name)

		# Upload the file
		try:
			resp = self._s3_client.upload_file(file_path, bucket_name, object_name)
			print("File uploaded")
		except botocore.exceptions.ClientError as e:
			print(e)
			return False
		return True

	def download_file(self, bucket_name=None, object_name=None, file_path=None):
		"""
		Download a file from S3 bucket
		:param bucket_name: str
		:param object_name: str
		:param file_path: str
		:return: True if the file was download, else False
		"""
		try:
			self._s3_resource.Object(bucket_name, object_name).download_file(file_path)
		except Exception as e:
			print(e)
			return False
		return True

	def delete_object(self, bucket_name=None, object_name=None):
		"""
		Delete an object from an S3 bucket
		:param bucket_name: str
		:param object_name: str
		:return: True if the referenced object was deleted, otherwise False
		"""
		# Delete the object
		try:
			self._s3_client.delete_object(Bucket=bucket_name, Key=object_name)
			print("Object deleted")
		except botocore.exceptions.ClientError as e:
			print(e)
			return False
		return True

	def _get_s3_object_path(self, bucket_name=None, object_name=None):
		return 's3://{0}/{1}'.format(bucket_name, object_name)
