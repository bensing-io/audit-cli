def evaluate(lines):
    outcome = ''
    message = ''
    for line in lines:
        if line.startswith('FROM'):
            outcome = 'passed'
            message = 'Dockerfile contains a valid FROM instruction.'
        else:
            outcome = 'failed'
            message = 'Dockerfile does not contain a valid FROM instruction'
    return outcome, message


def description():
    return 'Checks if a Dockerfile has a valid FROM instruction'


def procedure_type():
    return "standard"
