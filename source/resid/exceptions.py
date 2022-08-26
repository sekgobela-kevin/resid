

class ResidError(Exception):
    '''Base exception class for all resid errors'''
    pass

class SourceError(ResidError):
    pass

class InvalidUrlError(SourceError):
    pass

class FIlePathError(SourceError):
    pass

class InvalidFilePathError(FIlePathError):
    pass

class UnsupportedSourceError(SourceError):
    pass
