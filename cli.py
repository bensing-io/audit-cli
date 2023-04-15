import os
import argparse
import hashlib
import json
import sys
import traceback

from procedure import Procedure


class Audit:
    def __init__(self, audit_inputs):
        self.file_path = audit_inputs.file
        self.procedures_dir = audit_inputs.procedures
        self.output_dir = "./" if audit_inputs.out is None else audit_inputs.out
        self.procedures = []
        self.report = dict()

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

    def generate_report(self):
        procedure_count = len(self.procedures)
        executed_count = len([r for r in self.procedures if r.is_valid])
        passed_count = len([r for r in self.procedures if r.passed])
        failed_count = executed_count - passed_count
        all_pass = executed_count == passed_count

        self.report["passed"] = all_pass
        self.report["procedure_count"] = procedure_count
        self.report["executed_count"] = executed_count
        self.report["passed_count"] = passed_count
        self.report["failed_count"] = failed_count
        self.report["target_file"] = os.path.basename(self.file_path)
        self.report["target_file_fingerprint"] = hashlib.sha256(open(self.file_path, 'rb').read()).hexdigest()

        procedure_details = []
        for procedure in self.procedures:
            procedure_result = dict()
            if procedure.is_valid:
                procedure_result["outcome"] = "pass" if procedure.passed else "fail"
                procedure_result["description"] = procedure.description
                procedure_result["type"] = procedure.type
                procedure_result["file_name"] = procedure.file_name
                procedure_result["file_fingerprint"] = procedure.fingerprint
                procedure_result["message"] = procedure.message
                procedure_details.append(procedure_result)
            else:
                procedure_result["outcome"] = "inconclusive"
                procedure_result["description"] = f'{procedure.file_name} - Inconclusive'
                procedure_result["file_name"] = procedure.file_name
                procedure_result["file_fingerprint"] = procedure.fingerprint
                procedure_result["message"] = f"There was an issue with the procedure file: {procedure.invalid_message}"
                procedure_details.append(procedure_result)

        self.report["procedure_details"] = procedure_details
    # TODO: Update report outputs to include he total ran vs executed, and seperatre the guildienes, standards, and inconclusive
    def terminal_report(self):
        pass_fail_indicator = '\033[91m Failed \033[0m' if not self.report.get("passed") else '\033[92m Passed \033[0m'
        print("\n")
        print(f'Summary - {pass_fail_indicator}')
        print('-' * 20)
        print(f'Target File: {self.report.get("target_file")}')
        print('-' * 20)
        print(f'Total:\t{self.report.get("procedure_count")}')
        print(f'Exec:\t{self.report.get("executed_count")}')
        print(f'Pass:\t{self.report.get("passed_count")}')
        print(f'Fail:\t{self.report.get("failed_count")}')
        print('-' * 20)

        print("\n")
        print('{:<60} {:<10} {:<60}'.format('Procedure', 'Outcome', 'Message'))
        print('-' * 20)
        for procedure in self.report.get("procedure_details"):
            outcome = '\033[92m pass \033[0m' if procedure.get("outcome") == "pass" else '\033[91m fail \033[0m'
            print(f'{procedure.get("description"):<60} {outcome:<10} {procedure.get("message"):<60}')
        print("\n")

    def json_report(self):

        target = {
            'file': self.report.get("target_file"),
            'fingerprint': self.report.get("target_file_fingerprint")
        }

        summary = {
            'executed': self.report.get("executed_count"),
            'passed': self.report.get("passed_count"),
            'failed': self.report.get("failed_count"),
        }

        details = []
        for procedure in self.report.get("procedure_details"):
            details.append({
                'description': procedure.get("description"),
                'outcome': procedure.get("outcome"),
                'message': procedure.get("message"),
                'file': procedure.get("file_name"),
                'fingerprint': procedure.get("file_fingerprint"),
            })

        report = {
            'target': target,
            'summary': summary,
            'details': details
        }

        output_file = os.path.join(self.output_dir, 'audit-report.json')
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=4)

    def report_audit_results(self):
        self.generate_report()
        self.terminal_report()
        self.json_report()

    def run(self):
        try:
            self.load_procedures()
            self.evaluate_procedures()
            self.report_audit_results()
        except Exception as e:
            print(f"Error: {str(e)}")
            print(traceback.format_exc())
            sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CLI to evaluate a file against a set of procedures')
    parser.add_argument('-f', '--file', required=True, help='file to evaluate')
    parser.add_argument('-p', '--procedures', required=True, help='directory containing the audit procedure files')
    parser.add_argument('-o', '--out', required=False, help='directory to output JSON report')
    args = parser.parse_args()
    Audit(args).run()
