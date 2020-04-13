# S3Connector
Convenient wrapper for S3 connector with some basic functionality.


## Install with pip
```bash
$ pip install S3Connector
```

## Usage
1. Import the library.
    ```python
    from S3Connector import S3Connector
    ```
2. Create an instance by defining aws access credentials and region name. These parameters might not be needed, depending on the machine's access rights. 
    ```python
    S3 = S3Connector(
        aws_access_key_id="##########",
        aws_secret_access_key="##########",
        aws_region_name="##########",
    )
    ```
3. The imported module has several functions. Please refer to respective help for more information.

    1. ```S3.exists_bucket(bucket_name)```: checks if a bucket exists
    1. ```S3.create_bucket(bucket_name)```: creates a bucket
    1. ```S3.delete_bucket(bucket_name)```: deletes a bucket
    1. ```S3.download_file(bucket_name, object_name, file_path)```: download a file from S3 bucket
    1. ```S3.delete_object(bucket_name, object_name)```: delete an object from S3 bucket
    1. ```S3.get_list_of_buckets()```: get list of S3 buckets
    1. ```S3.get_list_of_objects(bucket_name)```: get list of S3 object summaries (upto 1000)
    1. ```S3.get_list_of_all_object_keys(bucket_name)```: get list of all S3 object keys


**&copy; 2020, [Samyak Ratna Tamrakar](https://www.linkedin.com/in/srtamrakar/)**.
