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
1. The imported module has several functions. Please refer to respective help for more information.

#### ```S3-Connector```

1. ```upload_file(file_path, bucket_name, object_name)```: upload a file to S3 bucket
1. ```download_file(bucket_name, object_name, file_path)```: download a file from S3 bucket
1. ```delete_object(bucket_name, object_name)```: delete an object from S3 bucket


* **&copy; Samyak Ratna Tamrakar** - [Github](https://github.com/srtamrakar), [LinkedIn](https://www.linkedin.com/in/srtamrakar/).