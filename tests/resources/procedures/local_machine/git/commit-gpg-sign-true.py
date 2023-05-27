def evaluate(lines):
    try:
        config_value = ""
        config_line = ""
        for line in lines:
            if line.startswith('commit.gpgsign'):
                config_line = line.strip()
                config_value = config_line.split('=')[1].strip()
                break
        if config_line == "":
            return 'inconclusive', 'The commit.gpgsign configuration value was not present in the git configuration.'
        elif config_value != "true":
            return 'failed', 'The commit.gpgsign is set to [false].'
        elif config_value == "true":
            return 'passed', f'The commit.gpgsign is set to [true]; the config setting is "{config_line}"'
    except Exception as e:
        return 'inconclusive', f'Could not determine if commit.gpgsign was set: Error - {str(e)}'


def description():
    return f'Git client must have GPG Commit Signing enabled'


def procedure_type():
    return "standard"
