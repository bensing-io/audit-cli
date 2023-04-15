import argparse

from domain.audit import Audit


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CLI to evaluate a file against a set of procedures')
    parser.add_argument('-f', '--file', required=True, help='file to evaluate')
    parser.add_argument('-p', '--procedures', required=True, help='directory containing the audit procedure files')
    parser.add_argument('-o', '--out', required=False, help='directory to output JSON report')
    args = parser.parse_args()
    Audit(args).run()
