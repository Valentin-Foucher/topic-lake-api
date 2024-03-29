from enum import Enum


class ApplicationExceptionReason(Enum):
    ALREADY_EXISTS = 1
    DOES_NOT_EXISTS = 2
    INVALID_INPUT = 3
    FORBIDDEN_ACTION = 4
