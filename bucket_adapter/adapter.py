"""adapter class."""

import import_string


class Adapter(object):
    """Adapter.

    Args:
        object ([object]): [main adapter class which calls the adaptee functions]
    """

    def __init__(self, settings_file):
        """__init__ function.

        Args:
            settings_file ([type]): [main configuration settings of the respective service being used (s3/gcp)]
        """
        self.settings = settings_file
        adaptee_classname = self.settings['NAME']
        mod = import_string(adaptee_classname)
        self.adaptee_obj = mod()
        self.authenticate = self.adaptee_obj.authenticate(
            options=self.settings)

    def upload(self, *args, **kwargs):
        """upload.

        Returns:
            [string]: [returns the url afer uploading the file to bucket]
        """
        return self.adaptee_obj.upload(
            *args, **kwargs, options=self.settings, client=self.authenticate)

    def download(self, *args, **kwargs):
        """download.

        Returns:
            [file]: [downlaod the file in the working directory]
        """
        return self.adaptee_obj.download(*args, **kwargs, options=self.settings, client=self.authenticate)

    def generate_signed_url(self, *args, **kwargs):
        """generate the signed url.

        Returns:
            [string]: [a signed url which expires in an hour]
        """
        return self.adaptee_obj.generate_signed_url(*args, **kwargs, options=self.settings, client=self.authenticate)

    def get_blob(self, *args, **kwargs):
        """give us a custom blob object.

        Returns:
            [object]: [a custom blob/resource object]
        """
        return self.adaptee_obj.get_blob(*args, **kwargs, options=self.settings, client=self.authenticate)

    def generate_signed_url_with_custom_expiry(self, *args, **kwargs):
        """generate the signed url with custom expiry.

        Returns:
            [string]: [returns the signed url with custom expiry]
        """
        return self.adaptee_obj.generate_signed_url_with_custom_expiry(*args, **kwargs, options=self.settings, client=self.authenticate)

    def download_to_file_pointer(self, *args, **kwargs):
        """download_to_file_pointer.

        Returns:
            [type]: [returns the file pointer]
        """
        return self.adaptee_obj.download_to_file_pointer(*args, **kwargs, options=self.settings, client=self.authenticate)
    
    def get_head_object(self, *args, **kwargs):
        """get_head_object.

        Returns:
            [type]: [returns the head object]
        """
        return self.adaptee_obj.get_head_object(*args, **kwargs, options=self.settings, client=self.authenticate)
