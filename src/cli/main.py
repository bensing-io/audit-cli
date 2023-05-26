"""The entrypoint for the NAPE cli"""
import argparse
import sys
import traceback

from src.cli.terminal_application import TerminalApplication


def main():
    """The function which 'nape' command invokes"""

    parser = argparse.ArgumentParser(
        description='CLI to evaluate a file against a set of procedures')
    parser.add_argument('-f', '--file', required=True,
                        help='file to evaluate')
    parser.add_argument('-p', '--procedures', required=True,
                        help='directory containing the audit procedure files')
    parser.add_argument('-o', '--out', required=False,
                        help='directory to output JSON report')

    try:
        args = parser.parse_args()
        terminal_app = TerminalApplication(args.file, args.procedures, args.out)
        terminal_app.run_app()
    except Exception as _exception:
        print(f"Error: {str(_exception)}")
        print(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    main()
