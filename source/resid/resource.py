from . import exceptions


class Resource(): 
    def __init__(self, source, content_type=None, encoding=None):
        self._source = source
        self._content_type = content_type
        self._encoding = encoding


    def _validate_source(self, source):
        # Raises exception when source is not supported
        if not self.source_supported(source):
            err_msg = "Source '{}' is not supported for {}"
            err_msg = err_msg.format(
                self.to_string(source)[:20], 
                type(self)
            )
            raise exceptions.UnsupportedSourceError(err_msg)

    def source_supported(self, source):
        # Checks if source is supported
        # Any object is supported and can be used as source
        return isinstance(source, object)

    def to_string(self, source):
        # Returns string version of source
        return str(source)

    def available_locally(self, source):
        # Checks if source data is available on this local machine
        return False

    def source_resembles(self, source):
        # Returns True if source is likely to be supported.
        # That does not mean source is supported.
        return self.source_supported(source)

    @property
    def supported(self):
        return self.source_supported(self._source)

    @property
    def resembles(self):
        return self.source_resembles(self._source)

    @property
    def issues(self):
        return self.supported or self.resembles

    @property
    def status(self):
        if self.supported:
            return "OK"
        elif self.source_resembles(self._source):
            return "Not Supported but resembles"
        else:
            return "Critically Not Supported"

    @property
    def locally(self):
        return self.available_locally(self._source)

    @property
    def remotely(self):
        return not self.available_locally(self._source)

    @property
    def uri(self):
        return self.to_string(self._source)
    
    @property
    def source(self):
        return self._source

    @property
    def content_type(self):
        return self._content_type

    @property
    def encoding(self):
        return self._encoding
