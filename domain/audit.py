import os
import json
import sys
import traceback

from domain.audit_outcome import AuditOutcome
from domain.audit_report import AuditReport
from domain.procedure import Procedure
from domain.reports.cli_terminal_report import CliTerminalReport


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
        # pass_fail_indicator = '\033[91m Failed \033[0m' if not self.report.outcome() == AuditOutcome.Passed \
        #     else '\033[92m Passed \033[0m'
        # print("\n")
        # print(f'Summary - {pass_fail_indicator}')
        # print('-' * 20)
        # print(f'Target File: {self.report.target_file()}')
        # print('-' * 20)
        # print(f'Total:\t{self.report.total()}')
        # print(f'Exec:\t{self.report.executed()}')
        # print(f'Pass:\t{self.report.passed()}')
        # print(f'Fail:\t{self.report.failed()}')
        # print('-' * 20)
        #
        # print("\n")
        # print('{:<60} {:<10} {:<60}'.format('Standards', 'Outcome', 'Message'))
        # print('-' * 20)
        # for procedure_result in self.report.standards_details():
        #     outcome = '\033[92m pass \033[0m' if procedure_result.outcome() == AuditOutcome.Passed \
        #         else '\033[91m fail \033[0m'
        #     print(f'{procedure_result.description():<60} {outcome:<10} {procedure_result.message():<60}')
        # print("\n")
        #
        # print("\n")
        # print('{:<60} {:<10} {:<60}'.format('Guidelines', 'Outcome', 'Message'))
        # print('-' * 20)
        # for procedure_result in self.report.guidelines_details():
        #     outcome = '\033[92m pass \033[0m' if procedure_result.outcome() == AuditOutcome.Passed \
        #         else '\033[91m fail \033[0m'
        #     print(f'{procedure_result.description():<60} {outcome:<10} {procedure_result.message():<60}')
        # print("\n")

    def json_report(self):

        target = {
            'file': self.report.target_file(),
            'fingerprint': self.report.target_file_fingerprint()
        }

        summary = {
            'total': self.report.total(),
            'executed': self.report.executed(),
            'passed': self.report.passed(),
            'failed': self.report.failed(),
        }

        standards = []
        for procedure_result in self.report.standards_details():
            standards.append({
                'description': procedure_result.description(),
                'outcome': procedure_result.outcome().value,
                'message': procedure_result.message(),
                'file': procedure_result.file_name(),
                'fingerprint': procedure_result.file_fingerprint(),
            })

        guidelines = []
        for procedure_result in self.report.guidelines_details():
            guidelines.append({
                'description': procedure_result.description(),
                'outcome': procedure_result.outcome().value,
                'message': procedure_result.message(),
                'file': procedure_result.file_name(),
                'fingerprint': procedure_result.file_fingerprint(),
            })

        details = {
            'standards': standards,
            'guidelines': guidelines
        }

        report = {
            'target': target,
            'summary': summary,
            'details': details
        }

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
