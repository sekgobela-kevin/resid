# Define high level functions for the project.
# Functions that are useful at high level are defined here.
# It include guessing content type, encoding and others.

from . import master


def find_resource(source, strict=True, **kwargs):
    # Find resource object closely related to source.
    # master contains resource objects created from source.
    # Returns None of source cannot satisfy any of resource object.
    master_obj = master.Master(source, **kwargs)
    # Gets supported resource from master.
    # Supported resource clearly matches the source.
    supported_resource = master_obj.supported_resource
    if supported_resource:
        return supported_resource
    elif not strict:
        # Gets resource resembling source.
        # Resemblimg sources are not guaranteed to be supported.
        # e.g url may still be invalid or file path not existing.
        return master_obj.resembles_resource

def _resource_access_attr(_resource, attribute, default=None):
    # Accesses attribute of resource object.
    # Takes into account resource being None(see find_resource())
    # 'default' argument will be returned in place of None.
    # If attribute does not exists exception will be raised.
    if _resource:
        value = getattr(_resource, attribute)
        if value != None:
            return value
    return default

def _find_resource_access_attr(source, attribute, strict=True, 
    default=None, **kwargs):
    # Finds resource object and access attribute from it.
    # None is returned when resource object cannot be found.
    # None also when the attribute has value of None(likely)
    resource_object = find_resource(source, strict, **kwargs)
    return _resource_access_attr(resource_object, attribute, default)

def guess_content_type(source) -> str:
    # Guesses content type of contents of source
    return _find_resource_access_attr(source, "content_type", False)

def guess_encoding(source):
    # Guesses encording of contents of source
    return _find_resource_access_attr(source, "encoding", False)

def locally_hosted(source):
    # Returns True if contents of source are available locally
    return _find_resource_access_attr(source, "locally", False)

def remotely_hosted(source):
    # Returns True if contents of source are available remotely.
    return _find_resource_access_attr(source, "remotely", False)

def is_supported(source):
    # Returns if source is supported(e.g is valid url)
    return _find_resource_access_attr(source, "supported", False, False)

def is_resembled(source):
    # Returns True if source resembles classes for supported sources.
    # Source may be valid file path but not existing.
     return _find_resource_access_attr(source, "resembles", False, False)

def to_string(source):
    # returns string version of source(None if not supported)
    return _find_resource_access_attr(source, "uri", False)

def guess_type(source):
    # Returns string about type of source provided source.
    # It may be files path, file like object, etc.
    return _find_resource_access_attr(source, "uri_type", False)

def guess_name(source):
    # Guesses name of source(string version of source)
    return to_string(source)


if __name__ == "__main__":
    resource = find_resource("file.py", False)
    print(guess_type("git://www.google.com/search?q=mimetypes+"))
    
