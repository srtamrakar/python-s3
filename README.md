# S3Connector
A S3 connector with some basic functionalities.

## Requirements

* Python 3+ (Tested in 3.7)
* boto3>=1.9.134
* botocore>=1.12.134


## Install with pip
```bash
$ pip install S3Connector
```

## Usage
1. Import the library.
    ```python
    from S3Connector import S3Connector
    ```
2. Create an instance by defining aws access credentials and region name. These parameters might not be needed, depending on the machine"s access rights. 
    ```python
    s3_connector = S3Connector(
        aws_access_key_id="##########",
        aws_secret_access_key="##########",
        aws_region="##########",
    )
    ```
3. The imported module has several functions. Please refer to respective help for more information.

    1. ```s3_connector.upload_file(file_path, bucket_name, object_name)```: upload a file to S3 bucket
    1. ```s3_connector.upload_dataframe_as_csv(dataframe, bucket_name, object_name, csv_sep, csv_null_identifier)```: upload a dataframe as csv to S3 bucket
    1. ```s3_connector.download_file(bucket_name, object_name, file_path)```: download a file from S3 bucket
    1. ```s3_connector.delete_object(bucket_name, object_name)```: delete an object from S3 bucket
    1. ```s3_connector.get_list_of_buckets()```: get list of S3 buckets
    1. ```s3_connector.get_list_of_objects(bucket_name)```: get list of S3 objects


* **&copy; Samyak Ratna Tamrakar** - [Github](https://github.com/srtamrakar), [LinkedIn](https://www.linkedin.com/in/srtamrakar/).
