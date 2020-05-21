class BucketDoesNotExistError(Exception):
    def __init__(self, bucket: str):
        self.bucket = bucket

    def __str__(self):
        return f"Bucket does not exist: '{self.bucket}'"


class CreateBucketError(Exception):
    def __init__(self, bucket: str):
        self.bucket = bucket

    def __str__(self):
        return f"Failed to create bucket '{self.bucket}'"


class DeleteBucketError(Exception):
    def __init__(self, bucket: str):
        self.bucket = bucket

    def __str__(self):
        return f"Failed to delete bucket '{self.bucket}'"


class UploadError(Exception):
    def __init__(self, file_path: str, bucket: str, object_key: str):
        self.file_path = file_path
        self.bucket = bucket
        self.object_key = object_key

    def __str__(self):
        return f"Failed to upload file '{self.file_path}' as '{self.bucket}/{self.object_key}'"


class DownloadError(Exception):
    def __init__(self, bucket: str, object_key: str, file_path: str):
        self.bucket = bucket
        self.object_key = object_key
        self.file_path = file_path

    def __str__(self):
        return f"Failed to download object '{self.bucket}/{self.object_key}' to '{self.file_path}'"


class DeleteObjectError(Exception):
    def __init__(self, bucket: str, object_key: str):
        self.bucket = bucket
        self.object_key = object_key

    def __str__(self):
        return f"Failed to delete object '{self.bucket}/{self.object_key}'"
