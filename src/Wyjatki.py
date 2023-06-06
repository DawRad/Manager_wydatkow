class OutOfBondsError(ValueError):
    def __init__(self, message):
        super().__init__(message)

class BadFileFormatError(ValueError):
    def __init__(self, message) -> None:
        super().__init__(message)