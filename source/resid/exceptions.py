

class ResidError(Exception):
    '''Base exception class for all resid errors'''
    pass

class SourceError(ResidError):
    pass

class InvalidUrlError(SourceError):
    pass

class InvalidFilePathError(SourceError):
    pass

class UnsupportedSourceError(SourceError):
    pass
