from . import filepath
from . import file_memory

from . import urlmod
from . import weburl

from . import exceptions


class DocumentURI(): 
    def __init__(self, source, path=None, content_type=None, encoding=None):
        self._source = source
        self._content_type = content_type
        self._encording = encoding
        self._setup_path(path)

    def _setup_path(self, path):
        # Setup _path attribute from path
        if path != None:
            self._path = path
        else:
            if self.source_supported(self._source):
                self._path = self.extract_path(self._source)
            else:
                err_msg = "Source '{}' is not supported for {}"
                err_msg = err_msg.format(self.to_string(), type(self))
                raise exceptions.UnsupportedSourceError(err_msg)

    def source_supported(self, source):
        # Checks if source is supported
        # Any object is supported and can be used as source
        return isinstance(source, object)

    def to_string(self):
        # Returns string version of source
        return str(self._source)

    def get_source(self):
        return self._source

    def extract_path(self, source):
        # Extarcts path from source
        raise NotImplementedError

    def get_path(self):
        return self._path

    def get_content_type(self):
        if self._content_type != None:
            return self._content_type
        else:
            return filepath.guess_content_type(self._path)

    def get_encoding(self):
        if self.self._encoding != None:
            return self._encoding
        else:
            return filepath.guess_encoding(self._path)


class WebUrl(DocumentURI):
    def get_content_type(self):
        # Retrieves content type of url
        if filepath.extract_extension(self._path):
            return super().get_content_type()
        else:
            # html file is basic structure for webpage.
            # content type for webpage is same as that of html
            return filepath.guess_content_type(" .html")
            

    def extract_path(self, url):
        # Extracts path from source
        return urlmod.extract_path(self._source)

    def source_supported(self, source):
        # Checks if source is valid url
        return weburl.is_web_url(source)

    def is_webpage(self):
        # Checks if source(url) points to webpage
        html_content_type = filepath.guess_content_type(" .html")
        return html_content_type == self.get_content_type()

    def get_hostname(self):
        return urlmod.extract_hostname(self._source)

    def get_netloc(self):
        return urlmod.extract_netloc(self._source)

    def get_scheme(self):
        return urlmod.extract_scheme(self._source)


class FilePath(DocumentURI):
    def extract_path(self, file_path):
        return file_path

    def source_supported(self, source):
        return filepath.is_file(source, True)


class FilePathURL(FilePath):
    def extract_path(self, file_path):
        return urlmod.extract_path(file_path)

    def source_supported(self, source):
        if urlmod.is_url(source, {"file"}):
            file_path = self.extract_path(source)
            return super().source_supported(file_path)
        else:
            return False

 
class FileMemory(DocumentURI):
    def extract_path(self, file_object):
        # Extracts path from 'name' attribute of file object.
        # Empty string will be returned if 'name' attributes not exists.
        try:
            name = file_object.name
        except AttributeError:
            return ""
        else:
            if isinstance(name, (str, bytes, os.PathLike)):
                return name
            else:
                return bytes(name)
    
    def source_supported(self, source):
        # Checks True if source is file like object
        return file_memory.is_memory_file(source)

    def to_string(self):
        # Returns string version of file object
        if self._path:
            return str(self._path)
        else:
            return str(self._source)


if __name__ == "__main__":
    import os
    import tempfile

    _file_path = "https://www.example.com/search.filenames"
    with tempfile.TemporaryFile() as f:
        file = FilePathURL("file:///home/kevin-ubuntu/projects/resid/setup.py")
        print(file.get_content_type())
        