"""AWS adapter."""

import logging
from datetime import datetime, timezone

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from dateutil.relativedelta import relativedelta

from bucket_adapter.custom_blob import CustomBlob


class AWS(object):
    """Main AWS adapter class.

    Args:
        object ([type]): [adaptee function to be called]
    """

    # Default signing version to be used.
    DEFAULT_VERSION = 's3v4'

    def _get_signature_version(self, options: dict) -> str:
        """return a valid signature version for use in signing.

        Args:
            options (dict): options dict contains all the configuration settings

        Returns:
            str: Defaults to s3v4 if not found in options.
        """
        version = options.get('SIGNATURE_VERSION', self.DEFAULT_VERSION)

    def authenticate(self, options):
        """authenticate function to authenticate the service (aws s3/gcp bucket).

        Args:
            options ([dict]): [options dict contains all the configuration settings]

        Returns:
            [object]: [a client object when authentication is successful else exception is raised]
        """
        try:
            client = boto3.client('s3',
                                  config=Config(
                                      signature_version=self._get_signature_version(options)),
                                  **options['CREDENTIALS'])
            return client
        except ClientError as e:
            logging.error(e)
            raise Exception('Authentication Failed')

    def upload(self, filename, options, client, bucket_filename=None, ExtraArgs=None):
        """Upload a file to an S3 bucket.

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        if bucket_filename is None:
            bucket_filename = filename
        try:
            client.upload_file(
                filename, options['BUCKET_NAME'], bucket_filename, ExtraArgs)
            # NOTE: S3 client does not return anything, so to make sure our interface
            # signature remains same, we will add a dummy url with file name.
            url_link = f'https://localhost/{bucket_filename}'
            return True, url_link
        except ClientError as e:
            logging.error(e)
            return False

    def download(self, filename, options, client, bucket_filename=None):
        """download file.

        Args:
            filename ([type]): [description]
            options ([type]): [description]
            object_name ([type], optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """
        try:
            if bucket_filename is None:
                bucket_filename = filename
            response = client.download_file(
                options['BUCKET_NAME'], bucket_filename, filename)
            # FIXME: return proper type.
            return ('File Downloaded in your working directory')
        except ClientError as e:
            logging.error(e)
            return None

    def generate_signed_url(self, filename, options, client, expiration=3600):
        """signed url with expiry of 1 hour.

        Args:
            filename ([string]): [description]
            options ([dict]): [options dict contains all the configuration settings]
            client ([object]): [a client object received after successful authentication]
            expiration (int, optional): [expiry of 1 hour by default]. Defaults to 3600.

        Returns:
            [type]: [description]
        """
        try:
            response = client.generate_presigned_url('get_object',
                                                     Params={'Bucket': options['BUCKET_NAME'],
                                                             'Key': filename},
                                                     ExpiresIn=expiration)
            return response
        except ClientError as e:
            logging.error(e)
            return None

    def get_blob(self, filename, options, client=None):
        """a resource object.

        Args:
            filename ([string]): [filename]
            options ([dict]): [options dict contains all the configuration settings]

        Returns:
            [object]: [a custom blob/resource object]
        """
        client = boto3.resource('s3',
                                aws_access_key_id=options['ACCESS_KEY'],
                                aws_secret_access_key=options['SECRET_KEY'],
                                config=Config(
                                    signature_version=self._get_signature_version(options))
                                )
        resource = client.Object(options['BUCKET_NAME'], filename)
        resource = CustomBlob(
            blob=resource, options=options, filename=filename)
        return resource

    def generate_signed_url_with_custom_expiry(self, filename, client, expiration, options):
        """signed url with custom expiry.

        Args:
            filename ([string]): [filenam to generate signed url]
            client ([object]): [a client object received after successful authentication]
            expiration ([datettime]): [custom expiry for the signed url]
            options ([dict]): [options dict contains all the configuration settings]

        Returns:
            [string]: [a signed url of the file you want to access (download)]
        """
        try:
            if not expiration:
                # defaulting to an hour
                expiration = datetime.utcnow().replace(tzinfo=timezone.utc) + \
                    relativedelta(seconds=3600)
            delta = expiration - datetime.utcnow().replace(tzinfo=timezone.utc)
            response = client.generate_presigned_url('get_object',
                                                     Params={'Bucket': options['BUCKET_NAME'],
                                                             'Key': filename},
                                                     ExpiresIn=delta.seconds)
            return response
        except ClientError as e:
            logging.error(e)
            return None

    def download_to_file_pointer(self, filename, tempfile_name, client, options):
        """download to file pointer.

        Args:
            filename ([string]): [description]
            client ([object]): [client object of the service used (aws s3/gcp bucket)]
            options ([dict]): [options dict that contains all the configuration settings]

        Returns:
            [type]: [description]
        """
        resource = boto3.resource('s3',
                                  aws_access_key_id=options['ACCESS_KEY'],
                                  aws_secret_access_key=options['SECRET_KEY'],
                                  config=Config(
                                      signature_version=self._get_signature_version(options))
                                  )
        bucket = resource.Bucket(options['BUCKET_NAME'])
        response = bucket.download_fileobj(filename, tempfile_name)
        return response

    def get_head_object(self, filename, options, client):
        """get head_object of s3 object.

        Args:
            Key ([string]): [file name]
            options ([dict]): [description]
            client ([dict]): [description]

        Returns:
            [dict]: [meta data of S3 object]
        """
        try:
            response = client.head_object(
                Bucket=options['BUCKET_NAME'], Key=filename)
            return True, response
        except ClientError as e:
            logging.error(e)
            return False, None
