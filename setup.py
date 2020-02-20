import os

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

module_version = "0.1.9"

setup(
    name="S3Connector",
    packages=["S3Connector"],
    version=module_version,
    license="MIT",
    description="A S3 connector with some basic functionalities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Samyak Ratna Tamrakar",
    author_email="samyak.r.tamrakar@gmail.com",
    url="https://github.com/srtamrakar/python-s3",
    download_url=f"https://github.com/srtamrakar/python-s3/archive/v_{module_version}.tar.gz",
    keywords=["aws", "s3"],
    install_requires=["boto3>=1.11.17", "botocore>=1.14.17"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Database :: Database Engines/Servers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
