import subprocess


def evaluate(lines):
    try:
        output = subprocess.check_output(['someCli'], stderr=subprocess.STDOUT)
        if output is not None:
            return {'outcome': 'failed', 'message': 'The program "someCli" is installed.'}
        else:
            return {'outcome': 'passed', 'message': 'The program "someCli" is not installed.'}
    except Exception as e:
        if "No such file or directory: 'someCli'" in str(e):
            return {'outcome': 'passed', 'message': 'The program "someCli" is not installed.'}
        else:
            return {'outcome': 'inconclusive', 'message': f'Unable to determine if "someCli" is installed. {e}.'}


def description():
    return 'Must not contain program "someCli"'


def procedure_type():
    return "standard"
