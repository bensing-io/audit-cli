import argparse
import sys
import traceback

from src.cli.terminal_application import TerminalApplication


def main():
    parser = argparse.ArgumentParser(description='CLI to evaluate a file against a set of procedures')
    parser.add_argument('-f', '--file', required=True, help='file to evaluate')
    parser.add_argument('-p', '--procedures', required=True, help='directory containing the audit procedure files')
    parser.add_argument('-o', '--out', required=False, help='directory to output JSON report')

    try:
        args = parser.parse_args()
        TerminalApplication(args.file, args.procedures, args.out).run()
    except Exception as e:
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    main()
