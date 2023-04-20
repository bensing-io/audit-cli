import subprocess


def description():
    return 'Must not contain program "someCli"'


def procedure_type():
    return "standard"


def evaluate(lines):
    try:
        output = subprocess.check_output(['someCli'], stderr=subprocess.STDOUT)
        if output is not None:
            return 'failed', 'The program "someCli" is installed.'
        else:
            return 'passed', 'The program "someCli" is not installed.'
    except Exception as e:
        if "No such file or directory: 'someCli'" in str(e):
            return 'passed', 'The program "someCli" is not installed.'
        else:
            return 'inconclusive', f'Unable to determine if "someCli" is installed. {str(e)}.'
