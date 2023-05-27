"""TerminalApplication is the application module which encapsulates the
NAPE terminal application code."""
import json
import os

from cli_terminal_report import CliTerminalReport
from json_report import JSONReport
from audit import Audit


class TerminalApplication:
    """This class has the responsibility for understanding the IO of how the files and
    procedures get loaded, and how to display the audit report."""

    def __init__(self, file_path, procedures_dir, json_output_dir):
        self._file_path = file_path
        self._procedures_dir = procedures_dir
        self._json_output_dir = json_output_dir

    def run_app(self):
        """The main method which manages the execution for the Terminal Application"""
        _audit = Audit(self._file_path, self._load_file(), self._load_procedures())
        _audit.execute()
        self._print_reports(_audit)

    def _load_file(self) -> []:
        _lines = []
        with open(self._file_path, 'r', encoding="UTF-8") as _file:
            _lines = _file.readlines()
        return _lines

    def _load_procedures(self) -> []:
        _procedures = []
        for root, _, files in os.walk(self._procedures_dir):
            for file_name in files:
                if file_name.endswith('.py'):
                    procedure_file = os.path.join(root, file_name)
                    from audit_procedure import AuditProcedure
                    _procedures.append(AuditProcedure(procedure_file))
        return _procedures

    def _print_reports(self, audit):
        CliTerminalReport(audit).generate_report()
        self._print_json_report(audit, self._json_output_dir)

    def _print_json_report(self, audit, json_output_dir):
        if self._json_output_dir is None:
            return
        json_report = JSONReport(audit).generate_report()
        if not os.path.exists(json_output_dir):
            os.makedirs(json_output_dir)
        output_file = os.path.join(json_output_dir, 'audit-report.json')
        with open(output_file, 'w', encoding="UTF-8") as _file:
            json.dump(json_report, _file, indent=4)