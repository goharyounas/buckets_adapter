""""Setup file."""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bucket_adapter",
    version="0.3.11rc1",
    author="Gohar Younas Malik",
    author_email="goharyounas@gmail.com",
    description="A generic adapter for gcp/aws services to upload/download files on bucket.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/goharyounas/buckets_adapter",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Developers',
        "Operating System :: OS Independent",
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    python_requires='>=3.7',
    install_requires=[
        'Django==3.0.8',
        'import_string',
        'google-cloud',
        'boto3'
    ]
)
