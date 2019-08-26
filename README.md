# S3-Connector
A S3 connector with some basic functionalities.

## Requirements

* Python 3+ (Tested in 3.7)
* boto3>=1.9.134
* botocore>=1.12.134


## Install with pip
```bash
$ pip install S3-Connector
```

## Usage
1. Import the library.
    ```python
    from S3-Connector import S3-Connector
    ```
2. Create an instance by defining the path for logfiles, the project name, the level of logging and whether to log to sys.stdout.
    ```python
    # parameters might not be needed, based on the access rights of machine 
    s3_connector = S3-Connector(
        aws_access_key_id='##########',
        aws_secret_access_key='##########',
        region_name='##########'
    )
    ```
3. The imported module has several functions. Please refer to respective help for more information.

    1. ```s3_connector.upload_file(file_path, bucket_name, object_name)```: upload a file to S3 bucket
    1. ```s3_connector.download_file(bucket_name, object_name, file_path)```: download a file from S3 bucket
    1. ```s3_connector.delete_object(bucket_name, object_name)```: delete an object from S3 bucket


* **&copy; Samyak Ratna Tamrakar** - [Github](https://github.com/srtamrakar), [LinkedIn](https://www.linkedin.com/in/srtamrakar/).