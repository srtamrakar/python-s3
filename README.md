# S3Connector
Convenient wrapper for S3 connector with some basic functionality.


## Install with pip
```bash
$ pip install S3Connector
```

## Usage
1.  Import the library.
    ```python
    from S3Connector import S3Connector
    ```
1.  AWS credentials are [fetched by boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html). Desired credentials can be passed while initializing `S3Connector`. In order to configure client connection, pass a [`botocore.config.Config`](https://botocore.amazonaws.com/v1/documentation/api/latest/reference/config.html) object.
    ```python
    S3 = S3Connector(
        aws_access_key_id="##########",
        aws_secret_access_key="##########",
        aws_region="##########",
        config=botocore.config.Config(
            connect_timeout=60,
            read_timeout=60,
        ),
    )
    ```
1.  The imported module has several functions.

    1. ```S3.exists_bucket(bucket)```: checks if a bucket exists
    1. ```S3.create_bucket(bucket)```: creates a bucket
    1. ```S3.delete_bucket(bucket)```: deletes a bucket
    1. ```S3.upload_file(file_path, bucket, object_key)```: upload a file to S3 bucket
    1. ```S3.download_file(bucket, object_key, file_path)```: download a file from S3 bucket
    1. ```S3.delete_object(bucket, object_key)```: delete an object from S3 bucket
    1. ```S3.get_bucket_list()```: get list of S3 buckets
    1. ```S3.get_object_list(bucket)```: get list of S3 object summaries (upto 1000)
    1. ```S3.get_object_key_list(bucket)```: get list of all S3 object keys


**&copy; 2020, [Samyak Ratna Tamrakar](https://www.linkedin.com/in/srtamrakar/)**.
