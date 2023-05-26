from enum import Enum


class AuditOutcome(Enum):
    PASSED = 'passed'
    FAILED = 'failed'
    INCONCLUSIVE = 'inconclusive'
    WARNING = 'warning'

    @classmethod
    def validate(cls, value: str) -> 'AuditOutcome':
        try:
            return cls(value.lower())
        except ValueError as _exception:
            raise ValueError(f'{_exception} is not a valid AuditOutcome') from _exception
