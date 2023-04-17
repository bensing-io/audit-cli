import os
import json
import sys
import traceback

from domain.audit_report import AuditReport
from domain.procedure import Procedure
from domain.reports.cli_terminal_report import CliTerminalReport
from domain.reports.json_report import JSONReport


class Audit:
    def __init__(self, audit_inputs):
        self.file_path = audit_inputs.file
        self.procedures_dir = audit_inputs.procedures
        self.output_dir = "./" if audit_inputs.out is None else audit_inputs.out
        self.procedures = []
        self.report = AuditReport

    def load_procedures(self):
        for root, _, files in os.walk(self.procedures_dir):
            for file_name in files:
                if file_name.endswith('.py'):
                    procedure_file = os.path.join(root, file_name)
                    self.procedures.append(Procedure(procedure_file))

    def evaluate_procedures(self):
        with open(self.file_path, 'r') as f:
            lines = f.readlines()
        for procedure in self.procedures:
            if procedure.is_valid:
                procedure.evaluate(lines)

    def report_audit_results(self):
        self.generate_report()
        self.terminal_report()
        self.json_report()

    def generate_report(self):
        self.report = AuditReport(self.file_path, self.procedures)

    def terminal_report(self):
        report = CliTerminalReport(self)
        report.generate_report()

    def json_report(self):
        json_report = JSONReport(self)
        report = json_report.generate_report()

        output_file = os.path.join(self.output_dir, 'audit-report.json')
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=4)

    def run(self):
        try:
            self.load_procedures()
            self.evaluate_procedures()
            self.report_audit_results()
        except Exception as e:
            print(f"Error: {str(e)}")
            print(traceback.format_exc())
            sys.exit(1)
