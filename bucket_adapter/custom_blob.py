"""custom blob."""


class CustomBlob(object):
    """CustomBlob to make a generic blob for both s3 & gcp bucket.

    Args:
        object ([type]): [description]
    """

    def __init__(self, blob, options, filename=None):
        """__init__ function to call the custom blob/resource function by determining the service type.

        Args:
            blob ([class object]): [blob object type s3/gcp]
            options ([dict]): [options dict contains all the configuration settings]
            filename ([string], optional): [filename used in s3 resource as it dont have any property like gcp blob.name and to make a custom & generic resource we need to add it.]. Defaults to None.
        """
        self.name = None
        self.time_created = None
        self.bucket = None
        self.content_type = None
        self.content_encoding = None
        self.content_language = None
        self.size = None
        print("TYPE:", type(blob), "is equal", )
        if type(blob) == Blob:
            self._generic_gcp_blob(blob, options)
        # Quick Hack because amazon uses generic factory functions to create
        # resource objects.
        elif str(type(blob)) == "<class 'boto3.resources.factory.s3.Object'>":
            self._generic_aws_resource(blob, options, filename=filename)
        # else:
        #     # custom function call
        #     func_pointer = options.get('BLOB_ETL_FUNCTION')
        #     func_pointer = import_string(func_pointer)
        #     func_pointer(self)

    def _generic_gcp_blob(self, blob, options, filename=None):
        """_generic_gcp_blob private function for custom gcp blob object.

        Args:
            blob ([object]): [blob object]
            options ([dict]): [options dict contains all the configuration settings]
            filename ([string], optional): [not used here as we have blob.name option in gcp blob object]. Defaults to None.
        """
        self.name = blob.name
        self.time_created = blob.time_created
        self.bucket = blob.bucket
        self.content_encoding = blob.content_encoding
        self.content_language = blob.content_language
        self.content_type = blob.content_type
        self.size = blob.size

    def _generic_aws_resource(self, blob, options, filename=None):
        """generic aws resource private function for custom s3 resource object.

        Args:
            blob ([object]): [resource object]
            options ([dict]): [options dict contains all the configuration settings]
            filename ([string], optional): [filename to be used in resource.name]. Defaults to None.
        """
        self.name = filename
        self.time_created = blob.last_modified
        self.bucket = options['BUCKET_NAME']
        self.content_encoding = blob.content_encoding
        self.content_language = blob.content_language
        self.content_type = blob.content_type
        self.size = blob.content_length
