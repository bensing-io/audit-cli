import hashlib
import os

from domain.audit_outcome import AuditOutcome
from domain.procedure_result import ProcedureResult


class AuditReport:

    def __init__(self, file_path, executed_procedures):
        self._total = len(executed_procedures)
        self._executed = len([r for r in executed_procedures if r.is_valid])
        self._passed = len([r for r in executed_procedures if r.outcome == AuditOutcome.Passed])
        self._outcome = self._determine_outcome(executed_procedures)
        self._procedure_details = self._process_procedure_details(executed_procedures)
        self._target_file = os.path.basename(file_path)
        self._target_fingerprint = hashlib.sha256(open(file_path, 'rb').read()).hexdigest()

    def total(self) -> int:
        return self._total

    def executed(self) -> int:
        return self._executed

    def passed(self) -> int:
        return self._passed

    def failed(self) -> int:
        return self._executed - self._passed

    def outcome(self) -> AuditOutcome:
        return self._outcome

    def target_file(self) -> str:
        return self._target_file

    def target_file_fingerprint(self) -> str:
        return self._target_fingerprint

    def procedure_details(self) -> []:
        return self._procedure_details

    def _determine_outcome(self, procedures) -> AuditOutcome:
        _outcome = ""
        _inconclusive = len([r for r in procedures if r.outcome == "inconclusive"])
        if _inconclusive is not None:
            _outcome = AuditOutcome.Inconclusive
        else:
            _outcome = AuditOutcome.Passed if self.executed() == self.passed() else AuditOutcome.Failed
        return _outcome

    def _process_procedure_details(self, procedures) -> []:
        _details = []
        for procedure in procedures:
            _details.append(ProcedureResult(procedure))
        return _details;

