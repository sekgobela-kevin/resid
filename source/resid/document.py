from . import pathmod
from . import filepath
from . import file_memory

from . import urlmod
from . import weburl

from . import resource
from . import exceptions

import os


# __all__ = [
#     "Document",
#     "WebURL",
#     "FilePath",
#     "FilePathLike",
#     "FilePathURL",
#     "FileMemory"
# ]

class Document(resource.Resource): 
    _path_types = pathmod.PATH_TYPES

    def __init__(self, source, content_type=None, encoding=None):
        super().__init__(source, content_type, encoding)

    def source_supported(self, source):
        # Checks if source is supported
        # Any object is supported and can be used as source
        return isinstance(source, object)

    def to_string(self, source):
        # Returns string version of source
        return str(source)

    def extract_path(self, source):
        # Extracts path from source
        raise NotImplementedError

    @property
    def path(self):
        return self.extract_path(self._source)

    @property
    def content_type(self):
        if self.path:
            return filepath.guess_content_type(self.path)

    @property
    def encoding(self):
        if super().encoding:
            return super().encoding
        elif self.content_type:
            # Guessses encoding from existing content type
            extension = filepath.guess_extension(self.content_type)
            if extension:
                return filepath.guess_encoding(" " + extension)


class URL(Document):
    _uri_type = "url"

    def extract_path(self, url):
        # Extracts path from source
        return urlmod.extract_path(self._source)

    def source_supported(self, source):
        # Checks if source is valid url
        return urlmod.is_url(source)

    def source_resembles(self, source):
        # Checks if source resembles url
        return urlmod.resembles_url(source)

    @property
    def hostname(self):
        return urlmod.extract_hostname(self._source)

    @property
    def netloc(self):
        return urlmod.extract_netloc(self._source)

    @property
    def scheme(self):
        return urlmod.extract_scheme(self._source)

    @property
    def query(self):
        return urlmod.extract_query(self._source)

    @property
    def params(self):
        return urlmod.extract_params(self._source)

    @property
    def fragment(self):
        return urlmod.extract_fragment(self._source)

    @property
    def port(self):
        return urlmod.extract_port(self._source)


class WebURL(Document):
    _uri_type = "web-url"

    @property
    def content_type(self):
        # Retrieves content type for contents of url
        if super().content_type:
            return super().content_type
        else:
            # html file is basic structure for webpage.
            # content type for webpage is same as that of html
            return filepath.guess_content_type(" .html")

    def source_supported(self, source):
        # Checks if source is valid url for web
        return weburl.is_web_url(source)

    def source_resembles(self, source):
        # Checks if source resembles url
        return weburl.resembles_web_url(source)

    @property
    def is_webpage(self):
        # Checks if source(url) points to webpage
        html_content_type = filepath.guess_content_type(" .html")
        return html_content_type == self.content_type
 


class Path(Document):
    _uri_type = "file-system-path"

    def __init__(self, source, content_type=None, encoding=None):
        super().__init__(source, content_type, encoding)
    
    def extract_path(self, path):
        if isinstance(path, os.PathLike):
            return path.name
        else:
            return path

    def source_supported(self, source):
        return pathmod.is_path(source, strict=True)

    def available_locally(self, path):
        return True

    def source_resembles(self, source):
        return pathmod.resembles_path(source)

    @property
    def size(self):
        return os.stat(self.path).st_size

    @property
    def access_time(self):
        return os.stat(self.path).st_atime

    @property
    def mod_time(self):
        return os.stat(self.path).st_mtime

    @property
    def create_time(self):
        return os.stat(self.path).st_ctime


class DirPath(Path):
    _uri_type = "dir-path"

    def source_supported(self, source):
        return pathmod.is_dir_path(source, strict=True)

    def source_resembles(self, source):
        return pathmod.resembles_dir(source)

    @property
    def files(self):
        return pathmod.get_folder_files(self._source, False)

    def dirs(self):
        return pathmod.get_folder_dirs(self._source, False)

    @property
    def dirs_recursive(self):
        return pathmod.get_folder_dirs(self._source, True)
    
    @property
    def files_recursive(self):
        return pathmod.get_folder_files(self._source, True)

class FilePath(Path):
    _uri_type = "file-path"
    def source_supported(self, source):
        # File path is expected to be string or bytes.
        # Pathlike, integers cant be used as path.
        return pathmod.is_file_path(source, strict=True)

    def source_resembles(self, source):
        # Checks if source resembles path
        return pathmod.resembles_file_path(source)

class PathLike(Path):
    _uri_type = "path-like-object"
    def extract_path(self, file_like):
        return file_like.name

    def source_supported(self, file_like):
        if isinstance(file_like, os.PathLike):
            file_path = self.extract_path(file_like)
            return super().source_supported(file_path)
        else:
            return False

    def source_resembles(self, source):
        return isinstance(source, os.PathLike)

class DirPathLike(PathLike):
    _uri_type = "dir-path-like-object"
    pass

class FilePathLike(PathLike):
    _uri_type = "file-path-like-object"
    pass

    

class FilePathURL(FilePath):
    _uri_type = "local-file-url"
    def extract_path(self, file_path):
        return urlmod.extract_path(file_path)

    def source_supported(self, source):
        if urlmod.is_url(source, {"file"}):
            file_path = self.extract_path(source)
            return super().source_supported(file_path)
        else:
            return False

    def source_resembles(self, source):
        return urlmod.resembles_url(source, {"file"})
 
class FileMemory(Document):
    _uri_type = "file-like-object"
    def set_path(self, path):
        # Sets associated with source
        if isinstance(path, self.path_types):
            self.path = path
        else:
            err_msg = "Path should be str, bytes or os.PathLike not {}"
            raise TypeError(err_msg.format(type(path)))


    def extract_path(self, file):
        # Extracts path from 'name' attribute of file object.
        # Empty string will be returned if 'name' attributes not exists.
        try:
            name = file._source.name
        except AttributeError:
            pass
        else:
            if isinstance(name, self.path_types):
                return name
    
    def source_supported(self, source):
        # Checks source satisfies requirements for file object.
        # 'name' attribute is expected to be valid path.
        return file_memory.is_memory_file(source)


    def to_string(self):
        # Returns string version of file object
        if self.path:
            return str(self.path)
        else:
            return ""

    def available_locally(self, file):
        return True


if __name__ == "__main__":
    import os
    import tempfile
    import pathlib

    _file_path = "https://www.example.com/search.filenames"
    with tempfile.TemporaryFile() as f:
        file = Path("setup\\")
        print(file.path)
        #file.set_path("filename.pdf")
        print(file.content_type, file.status)
            