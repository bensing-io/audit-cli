def evaluate(lines):
    for line in lines:
        if line.startswith('FROM'):
            return {'outcome': 'passed', 'message': f'Dockerfile contains a valid FROM instruction.'}
        else:
            return {'outcome': 'failed', 'message': f'Dockerfile does not contain a valid FROM instruction'}


def description():
    return 'Checks if a Dockerfile has a valid FROM instruction'


def procedure_type():
    return "standard"
