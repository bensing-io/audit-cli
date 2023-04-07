def evaluate(lines):
    found_from = False
    for line in lines:
        if line.startswith('FROM'):
            found_from = True
            break

    if not found_from:
        raise ValueError('Dockerfile does not contain a valid FROM instruction')

def description():
    return 'Checks if a Dockerfile has a valid FROM instruction'