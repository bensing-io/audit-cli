import subprocess

expected_java_version = "openjdk 19.0.2"


def evaluate(lines):
    try:
        version_query = subprocess.check_output(['java', '--version'],
                                                stderr=subprocess.STDOUT, universal_newlines=True)
        if expected_java_version in version_query:
            return 'passed', f'Local machine contains Java version [{expected_java_version}].'
        else:
            return 'failed', f'The installed java version is not correct.'
    except Exception as e:
        return 'inconclusive', f'Could not determine if Java was installed: Error - {str(e)}'


def description():
    return f'Validate Java version [{expected_java_version}] is installed.'


def procedure_type():
    return "standard"
