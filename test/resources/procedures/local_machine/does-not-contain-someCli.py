import subprocess


def evaluate(lines):
    try:
        output = subprocess.check_output(['someCli'], stderr=subprocess.STDOUT)
        if output is not None:
            return {'passed': False, 'message': 'The program "someCli" is installed.'}
        else:
            return {'passed': True, 'message': 'The program "someCli" is not installed.'}
    except Exception as e:
        if "No such file or directory: 'someCli'" in str(e):
            return {'passed': True, 'message': 'The program "someCli" is installed.'}
        else:
            return {'passed': False, 'message': f'Unable to determine if "someCli" is installed. {e}.'}


def description():
    return 'Must not contain program "someCli"'
