from enum import Enum


class AuditOutcome(Enum):
    Passed = 'passed'
    Failed = 'failed'
    Inconclusive = 'inconclusive'
    Warning = 'warning'

    @classmethod
    def validate(cls, value: str) -> 'AuditOutcome':
        try:
            return cls(value.lower())
        except ValueError:
            raise ValueError(f"{value} is not a valid AuditOutcome")