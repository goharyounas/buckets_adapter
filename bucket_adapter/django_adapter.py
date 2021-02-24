"""django adapter."""

from django.conf import settings

from .adapter import Adapter

settings_file = settings.BUCKET_ADAPTER_SETTING

generic_adapter = Adapter(settings_file)
