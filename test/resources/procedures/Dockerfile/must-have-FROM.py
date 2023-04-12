def evaluate(lines):
    for line in lines:
        if line.startswith('FROM'):
            return {'passed': True, 'message': f'Dockerfile contains a valid FROM instruction.'}
        else:
            return {'passed': False, 'message': f'Dockerfile does not contain a valid FROM instruction'}


def description():
    return 'Checks if a Dockerfile has a valid FROM instruction'
