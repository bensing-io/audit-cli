from src.kernel.audit_outcome import AuditOutcome


class ProcedureResult:

    def __init__(self, procedure):
        self.procedure = procedure

    def outcome(self) -> str:
        if self.procedure.is_valid:
            _outcome = self.procedure.outcome
        else:
            _outcome = AuditOutcome.Inconclusive
        return _outcome

    def description(self) -> str:
        _description = ""
        if not self.procedure.is_valid:
            _description = f'{self.file_name()} - Inconclusive'
        else:
            _description = "" if self.procedure.description is None else self.procedure.description
        return _description

    def message(self) -> str:
        _message = ""
        if not self.procedure.is_valid:
            _message = f'There was an issue with the procedure file: {self.procedure.invalid_message}'
        else:
            _message = "" if self.procedure.message is None else self.procedure.message
        return _message

    def type(self) -> str:
        return "" if self.procedure.type is None else self.procedure.type

    def file_name(self) -> str:
        return "" if self.procedure.file_name is None else self.procedure.file_name

    def file_fingerprint(self) -> str:
        return "" if self.procedure.fingerprint is None else self.procedure.fingerprint




