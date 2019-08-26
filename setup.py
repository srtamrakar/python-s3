import os

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

setup(
	name='S3-Connector',
	packages=['S3-Connector'],
	version='0.0.1',
	license='MIT',
	description='Some special functions for some python objects.',
	long_description=long_description,
	long_description_content_type='text/markdown',
	author='Samyak Ratna Tamrakar',
	author_email='samyak.r.tamrakar@gmail.com',
	url='https://github.com/srtamrakar/python-s3',
	# download_url = 'https://github.com/srtamrakar/python-s3/archive/v_0.0.1.tar.gz',
	keywords=['list', 'string', 'datetime', 'directory'],
	install_requires=[
		'boto3>=1.9.134',
		'botocore>=1.12.134',
	],
	classifiers=[
		'Development Status :: 2 - Pre-Alpha',  # Either"3 - Alpha", "4 - Beta" or "5 - Production/Stable"
		'Intended Audience :: Developers',  # Define that your audience are developers
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7'
	],
)
