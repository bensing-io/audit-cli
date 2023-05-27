from enum import Enum


class Outcome(Enum):
    PASSED = 'passed'
    FAILED = 'failed'
    INCONCLUSIVE = 'inconclusive'
    WARNING = 'warning'

    @classmethod
    def validate(cls, value: str) -> 'Outcome':
        try:
            return cls(value.lower())
        except ValueError as _exception:
            raise ValueError(f'{_exception} is not a valid Outcome') from _exception
