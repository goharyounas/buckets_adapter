"""GCP class file."""

import datetime
import json
import logging
import os

from google.cloud import exceptions, storage
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials

from bucket_adapter.custom_blob import CustomBlob


class GCP(object):
    """GCP.

    Args:
        object ([type]): [description]

    Returns:
        [object]: [custom blob/resource object]
    """

    REQUIRED_FIELDS = ['CREDENTIAL_FILE', 'PROJECT_NAME', 'BUCKET_NAME']

    def authenticate(self, options):
        """[authenticate function to authenticate the service (aws s3/gcp bucket)].

        Args:
            options ([dict]): [options dict contains all the configuration settings]

        Returns:
            [object]: [a client object when authentication is successful else exception is raised]
        """
        try:
            credentials = None
            if 'CREDENTIAL_JSON' in options and options['CREDENTIAL_JSON']:
                credentials = service_account.Credentials.from_service_account_info(
                    json.loads(options['CREDENTIAL_JSON']))
            else:
                credentials = service_account.Credentials.from_service_account_file(
                    options['CREDENTIAL_FILE'])
            if credentials:
                client = storage.Client(
                    credentials=credentials, project=options['PROJECT_NAME'])
            else:
                raise exceptions.Forbidden('Authentication Failed')
            if client:
                return client
            else:
                raise exceptions.GoogleCloudError('Authentication Failed')
        except Exception as E:
            logging.exception("Exception {err}".format())
            raise Exception('Authentication Failed')

    def upload(self, filename, options, client, bucket_filename=None, ExtraArgs=None):
        """upload function to uplaod the file to gcp bucket.

        Args:
            filename ([string]): [file to be uploaded to bucket]
            options ([dict]): [options dict contains all the configuration settings]

        Returns:
            [tuple]: [bool success and uploaded file bucket url ]
        """
        try:
            if bucket_filename is None:
                bucket_filename = filename
            bucket = client.get_bucket(options['BUCKET_NAME'])
            blob = bucket.blob(bucket_filename)
            blob.upload_from_filename(filename)
            return True, blob.public_url
        except Exception as E:
            logging.error("Exception {err}".format(err=str(E)))

    def download(self, filename, options, client):
        """[download function to download the file in your working directory].

        Args:
            filename ([string]): [file to be download]
            options ([dict]): [dict object containing all the configuration settings]
            client ([object]): [client object received after successful authentication]

        Returns:
            [file]: [file is being downloaded in the working directory]
        """
        bucket = client.get_bucket(options['BUCKET_NAME'])
        blob = bucket.get_blob(filename)
        # FIXME: storage_name not defined?
        return blob.download_to_filename(storage_name)

    def generate_signed_url(self, filename, options, client):
        """Generate a v2 signed URL for downloading a blob.

        Note that this method requires a service account key file. You can not use
        this if you are using Application Default Credentials from Google Compute
        Engine or from the Google Cloud SDK.


        Args:
            file_name ([string]): [filename to be downloaded from bucket]
            options ([dict]): [options dict contains all the configuration settings]

        Returns:
            [string]: [a signed URL from where you can download the file and see it content]
        """
        bucket = client.bucket(options['BUCKET_NAME'])
        blob = bucket.blob(blob_name=filename)
        url = blob.generate_signed_url(
            expiration=datetime.timedelta(hours=1),
            method="GET",
        )
        return url

    def get_blob(self, filename, options, client):
        """[get custom blob object].

        Args:
            filename ([string]): [filename]
            options ([dict]): [options dict contains all the configuration settings]
            client ([object]): [client object received after successful authentication]

        Returns:
            [object]: [a custom blob object]
        """
        bucket = client.get_bucket(options['BUCKET_NAME'])
        blob = bucket.get_blob(filename)
        blob = CustomBlob(blob=blob, options=options)
        return blob

    def generate_signed_url_with_custom_expiry(self, filename, client, expiration, options):
        """[generate_signed_url_with_custom_expiry by passing the file expiry time as well].

        Args:
            filename ([string]): [file to be ]
            client ([object]): [client object received after successful authentication]
            expiration ([string]): [custom expiry to be set for the signed url]
            options ([dict]): [options dict contains all the configuration settings]

        Returns:
            [string]: [a signed url]
        """
        bucket = client.bucket(options['BUCKET_NAME'])
        blob = bucket.blob(blob_name=filename)
        url = blob.generate_signed_url(
            expiration=expiration,
            method="GET",
        )
        return url

    def download_to_file_pointer(self, filename, tempfile_name, client, options):
        """download to file pointer.

        Args:
            filename ([string]): [description]
            client ([object]): [client object of the service used (aws s3/gcp bucket)]
            options ([dict]): [options dict that contains all the configuration settings]

        Returns:
            [type]: [temporary file pointer object]
        """
        bucket = client.get_bucket(options['BUCKET_NAME'])
        blob = bucket.get_blob(filename)
        response = client.download_blob_to_file(blob, tempfile_name)
        return response

    def get_head_object(self, Key, options, client):
        """get head_object of GCP cloud storage object.

        Args:
            Key ([string]): [file name]
            options ([dict]): [description]
            client ([dict]): [description]
        """
        # FIXME
        raise NotImplementedError('Not Implemented on GCP')
