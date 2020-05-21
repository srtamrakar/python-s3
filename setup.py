import os
import re
from setuptools import setup, find_packages

ROOT = os.path.dirname(__file__)
MODULE_NAME = "S3Connector"


def get_author() -> str:
    author_re = re.compile(r"""__author__ = ['"]([A-Za-z .]+)['"]""")
    init = open(os.path.join(ROOT, MODULE_NAME, "__init__.py")).read()
    return author_re.search(init).group(1)


def get_version() -> str:
    version_re = re.compile(r"""__version__ = ['"]([0-9.]+)['"]""")
    init = open(os.path.join(ROOT, MODULE_NAME, "__init__.py")).read()
    return version_re.search(init).group(1)


def get_description() -> str:
    with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as f:
        description = f.read()
    return description


REQUIRED_LIBRARIES = ["boto3>=1.12.37", "botocore>=1.15.39"]


setup(
    name=MODULE_NAME,
    packages=find_packages(),
    version=get_version(),
    license="MIT",
    description="Convenient wrapper for S3 connector with some basic functionality.",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    author=get_author(),
    url="https://github.com/srtamrakar/python-s3",
    download_url=f"https://github.com/srtamrakar/python-s3/archive/v_{get_version()}.tar.gz",
    keywords=["aws", "s3"],
    install_requires=REQUIRED_LIBRARIES,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Database :: Database Engines/Servers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
