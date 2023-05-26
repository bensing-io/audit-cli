"""Audit is the use case which manages the execution of procedures against the target file"""
from typing import Type

from audit_report import AuditReport


class Audit:
    """
    Audit is the use case which manages the execution of procedures against the target file
    ...

    Attributes
    ---
    file_path: str
        the local file path to the target file which is being audited
    file_lines: arrary
        the lines of the target file
    procedures: array
        all of the procedures to evaluate the target file against

    """
    def __init__(self, file_path, file_lines, procedures):
        self._file_path = file_path
        self._file_lines = file_lines
        self._procedures = procedures
        self._report = AuditReport

    def execute(self):
        """
        Invokes all the procedures and generates an AuditReport once all procedures are ran
        """
        self._evaluate_procedures(self._file_lines)
        self._generate_report(self._file_path, self._procedures)

    def get_report(self) -> Type[AuditReport]:
        """
        Retrieve the AuditReport generated after the Audit execution.
        """
        return self._report

    def _evaluate_procedures(self, file_lines):
        for procedure in self._procedures:
            if procedure.is_valid:
                procedure.evaluate(file_lines)

    def _generate_report(self, file_path, procedures):
        self._report = AuditReport(file_path, procedures)
