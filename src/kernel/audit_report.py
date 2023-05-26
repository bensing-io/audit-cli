"""AuditReport takes all of the executed proceudres and aggregates execution state data"""

import hashlib
import os

from src.kernel.audit_outcome import AuditOutcome
from src.kernel.procedure_result import ProcedureResult


class AuditReport:
    """AuditReport takes all of the executed proceudres and aggregates execution state data"""

    def __init__(self, file_path, executed_procedures):
        self._total = len(executed_procedures)
        self._executed = len(
            [r for r in executed_procedures if r.is_valid])
        self._passed = len(
            [r for r in executed_procedures if r.outcome == AuditOutcome.PASSED])
        self._failed = len(
            [r for r in executed_procedures if r.outcome == AuditOutcome.FAILED])
        self._inconclusive = len(
            [r for r in executed_procedures if r.outcome == AuditOutcome.INCONCLUSIVE])
        self._outcome = self._determine_outcome(executed_procedures)
        self._standards_details, self._guidelines_details = \
            self._process_procedure_details(executed_procedures)
        self._target_file = os.path.basename(file_path)
        self._target_fingerprint = hashlib.sha256(open(file_path, 'rb').read()).hexdigest()

    def total(self) -> int:
        """Retrieves the total quantity of loaded procedures"""
        return self._total

    def executed(self) -> int:
        """Retrieves the total quantity of executed procedures"""
        return self._executed

    def passed(self) -> int:
        """Retrieves the total quantity of executed procedures which passed"""
        return self._passed

    def failed(self) -> int:
        """Retrieves the total quantity of executed procedures which failed"""
        return self._failed

    def inconclusive(self) -> int:
        """Retrieves the total quantity of executed procedures which were inconclusive"""
        return self._inconclusive

    def outcome(self) -> AuditOutcome:
        """Retrieves the outcome of audit: Passed, Failed, or Inconclusive"""
        return self._outcome

    def target_file(self) -> str:
        """Retrieves the name of the file which was audited"""
        return self._target_file

    def target_file_fingerprint(self) -> str:
        """Retrieves the fingerprint of the file which was audited"""
        return self._target_fingerprint

    def standards_details(self) -> []:
        """Retrieves all the procedures which are Standards"""
        return self._standards_details

    def guidelines_details(self) -> []:
        """Retrieves all the procedures which are Guidelines"""
        return self._guidelines_details

    def _determine_outcome(self, procedures) -> AuditOutcome:
        _outcome = ""
        _inconclusive = len([r for r in procedures if r.outcome == AuditOutcome.INCONCLUSIVE])
        if _inconclusive > 0:
            _outcome = AuditOutcome.INCONCLUSIVE
        else:
            _outcome = AuditOutcome.PASSED if self.executed() == self.passed() \
                else AuditOutcome.FAILED
        return _outcome

    def _process_procedure_details(self, procedures) -> []:
        _standards = []
        _guidelines = []
        for procedure in procedures:
            _procedure = ProcedureResult(procedure)
            if procedure.type == "standard":
                _standards.append(_procedure)
            elif procedure.type == "guideline":
                _guidelines.append(_procedure)
        return _standards, _guidelines
