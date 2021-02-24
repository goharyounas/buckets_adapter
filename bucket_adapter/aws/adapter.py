"""AWS adapter."""

import logging

import boto3
from botocore.exceptions import ClientError

from bucket_adapter.custom_blob import CustomBlob


class AWS(object):
    """Main AWS adapter class.

    Args:
        object ([type]): [adaptee fucntion to be called]
    """

    def authenticate(self, options):
        """authenticate function to authenticate the service (aws s3/gcp bucket).

        Args:
            options ([dict]): [options dict contains all the configuration settings]

        Returns:
            [object]: [a client object when authentication is successful else exception is raised]
        """
        try:
            s3_client = boto3.client('s3',
                                     aws_access_key_id=options['ACCESS_KEY'],
                                     aws_secret_access_key=options['SECRET_KEY'])
            return s3_client
        except ClientError as e:
            logging.error(e)
            raise Exception('Authentication Failed')

    def upload(self, filename, options, client, bucket_filename=None):
        """Upload a file to an S3 bucket
        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        if bucket_filename is None:
            bucket_filename = filename
        try:
            response = client.upload_file(
                filename, options['BUCKET_NAME'], bucket_filename)
            return ('File Uploaded on AWS S3 Bucket')
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

    def get_blob(self, filename, options):
        """a resource object.

        Args:
            filename ([string]): [filename]
            options ([dict]): [options dict contains all the configuration settings]

        Returns:
            [object]: [a custom blob/resource object]
        """
        client = boto3.resource('s3',
                                aws_access_key_id=options['ACCESS_KEY'],
                                aws_secret_access_key=options['SECRET_KEY'])
        resource = client.Object(options['BUCKET_NAME'], filename)
        resource = CustomBlob(
            blob=resource, options=options, filename=filename)
        return resource

    def generate_signed_url_with_custom_expiry(self, filename, client, expiration, options):
        """signed url with custom expiry.

        Args:
            filename ([string]): [filenam to generate signed url]
            client ([object]): [a client object received after successful authentication]
            expiration ([int]): [custom expiry for the signed url]
            options ([dict]): [options dict contains all the configuration settings]

        Returns:
            [string]: [a signed url of the file you want to access (download)]
        """
        try:
            expiration = time.now() + expiration
            response = client.generate_presigned_url('get_object',
                                                     Params={'Bucket': options['BUCKET_NAME'],
                                                             'Key': filename},
                                                     ExpiresIn=expiration.isoformat())
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
                                  aws_secret_access_key=options['SECRET_KEY'])
        bucket = resource.Bucket(options['BUCKET_NAME'])
        response = bucket.download_fileobj(filename, tempfile_name)
        return response
