import os
import argparse
import hashlib
import json
import sys

class Rule:
    def __init__(self, rule_file):
        self.rule_file = rule_file
        self.rule_name = os.path.basename(rule_file)
        self.passed = False
        self.description = None
        self.fingerprint = hashlib.sha256(open(rule_file, 'rb').read()).hexdigest()

        module_name = os.path.splitext(os.path.basename(rule_file))[0]
        sys.path.append(os.path.dirname(rule_file))
        module = __import__(module_name)
        self.evaluate_method = getattr(module, 'evaluate')
        self.description_method = getattr(module, 'description')

    def evaluate(self, file_path):
        try:
            self.evaluate_method(file_path)
            self.passed = True
        except:
            self.passed = False

    def get_description(self):
        self.description = self.description_method()

class Audit:
    def __init__(self):
        self.rules = []
        self.file_path = None
        self.rules_dir = None
        self.output_dir = None

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='CLI to evaluate a file against a set of rules')
        parser.add_argument('-f', '--file', required=True, help='file to evaluate')
        parser.add_argument('-r', '--rules', required=True, help='directory containing the Python rule files')
        parser.add_argument('-o', '--out', required=False, help='directory to output JSON report')
        args = parser.parse_args()
        self.file_path = args.file
        self.rules_dir = args.rules
        self.output_dir = args.out

    def load_rules(self):
        for file_name in os.listdir(self.rules_dir):
            if file_name.endswith('.py'):
                rule_file = os.path.join(self.rules_dir, file_name)
                self.rules.append(Rule(rule_file))

    def evaluate_file(self):
        with open(self.file_path, 'r') as f:
            lines = f.readlines()
        for rule in self.rules:
            rule.evaluate(lines)

    def get_rule_descriptions(self):
        for rule in self.rules:
            rule.get_description()

    def print_report(self):
        ruleCount = len(self.rules)
        passedCount = len([r for r in self.rules if r.passed])
        failedCount = ruleCount - passedCount
        allPass = ruleCount == passedCount 

        targetFile = os.path.basename(self.file_path)
        fileFingerprint = hashlib.sha256(open(self.file_path, 'rb').read()).hexdigest()

        passFail = '\033[92m Passed \033[0m' if allPass else '\033[91m Failed \033[0m'
        print("\n")
        print(f'Summary - {passFail}')
        print('-' * 20)
        print(f'Target File: {targetFile}')
        print(f'File Fingerprint: {fileFingerprint}')
        print('-' * 20)
        print(f"Total:\t{ruleCount}")
        print(f"Pass:\t{passedCount}")
        print(f"Fail:\t{failedCount}")
        print('-' * 20)

        print("\n")
        print('{:<60} {:<10} {:<20} {:<64}'.format('Rule', 'Outcome', 'File', 'Fingerprint'))
        print('-' * 20)
        for rule in self.rules:
            outcome = '\033[92m pass \033[0m' if rule.passed else '\033[91m fail \033[0m'
            print('{:<60} {:<10} {:<20} {:<64}'.format(rule.description, outcome, rule.rule_name, rule.fingerprint))
        print("\n")

    def json_report(self):

        target = {
            'file': os.path.basename(self.file_path),
            'fingerprint': hashlib.sha256(open(self.file_path, 'rb').read()).hexdigest()
        }

        summary = {
            'rules_executed': len(self.rules),
            'rules_passed': len([r for r in self.rules if r.passed]),
            'rules_failed': len([r for r in self.rules if not r.passed])
        }

        details = []
        for rule in self.rules:
            details.append({
                'rule': rule.description,
                'outcome': 'pass' if rule.passed else 'fail',
                'file': rule.rule_name,
                'fingerprint': rule.fingerprint
            })

        report = {
            'target': target,
            'summary': summary,
            'details': details
        }

        output_file = os.path.join(self.output_dir, 'audit-report.json')
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=4)

    def create_report(self):
        self.print_report()
        self.json_report()
   
    def run(self):
        try:
            self.parse_arguments()
            self.load_rules()
            self.evaluate_file()
            self.get_rule_descriptions()
            self.create_report()
        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)

if __name__ == '__main__':
    Audit().run()
