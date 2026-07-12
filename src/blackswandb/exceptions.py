class BlackSwanDBError(Exception):
    pass

class UnsupportedFormatError(BlackSwanDBError):
    pass

class DatasetNotFoundError(BlackSwanDBError):
    pass