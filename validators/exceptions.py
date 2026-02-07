from eth_utils.exceptions import ValidationError

class InvalidTypeData(ValidationError):
    pass

class InvalidTypeString(ValidationError):
    pass

class InvalidBinaryData(ValidationError):
    pass

class NotChecksumString(ValidationError):
    pass

class NotCorrectString(ValidationError):
    pass
