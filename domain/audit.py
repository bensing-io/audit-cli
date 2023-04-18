from typing import Type

from domain.audit_report import AuditReport


class Audit:
    def __init__(self, file_path, file_lines, procedures):
        self._file_path = file_path
        self._file_lines = file_lines
        self._procedures = procedures
        self._report = AuditReport

    def execute(self):
        self._evaluate_procedures(self._file_lines)
        self._generate_report(self._file_path, self._procedures)

    def get_report(self) -> Type[AuditReport]:
        return self._report

    def _evaluate_procedures(self, file_lines):
        for procedure in self._procedures:
            if procedure.is_valid:
                procedure.evaluate(file_lines)

    # TODO - Refactor out the file_path and make it the file_name; update the attributes
    def _generate_report(self, file_path, procedures):
        self._report = AuditReport(file_path, procedures)
