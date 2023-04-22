import json
import os
# TODO - figure out how to lini the kernel with the cli app
from ..nape_kernel.audit import Audit
from ..nape_kernel.procedure import Procedure
from reports.cli_terminal_report import CliTerminalReport
from reports.json_report import JSONReport


# This class has the responsibility for understanding the IO of how the files and procedures get loaded, and how to
# display the audit report.
class TerminalApplication:

    def __init__(self, file_path, procedures_dir, json_output_dir):
        self._file_path = file_path
        self._procedures_dir = procedures_dir
        self._json_output_dir = json_output_dir

    def _load_file(self) -> []:
        _lines = []
        with open(self._file_path, 'r') as f:
            _lines = f.readlines()
        return _lines

    def _load_procedures(self) -> []:
        _procedures = []
        for root, _, files in os.walk(self._procedures_dir):
            for file_name in files:
                if file_name.endswith('.py'):
                    procedure_file = os.path.join(root, file_name)
                    _procedures.append(Procedure(procedure_file))
        return _procedures

    def run(self):
        _audit = Audit(self._file_path, self._load_file(), self._load_procedures())
        _audit.execute()
        self._print_reports(_audit)

    def _print_reports(self, audit):
        self._print_terminal_report(audit)
        self._print_json_report(audit, self._json_output_dir)

    def _print_terminal_report(self, audit):
        CliTerminalReport(audit).generate_report()

    def _print_json_report(self, audit, json_output_dir):
        if self._json_output_dir is None:
            return
        json_report = JSONReport(audit).generate_report()
        if not os.path.exists(json_output_dir):
            os.makedirs(json_output_dir)
        output_file = os.path.join(json_output_dir, 'audit-report.json')
        with open(output_file, 'w') as f:
            json.dump(json_report, f, indent=4)
