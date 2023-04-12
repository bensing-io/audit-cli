import subprocess

expected_java_version = "openjdk 19.0.2"


def evaluate(lines):
    try:
        version_query = subprocess.check_output(['java', '--version'],
                                                stderr=subprocess.STDOUT, universal_newlines=True)
        if expected_java_version in version_query:
            return {'passed': True, 'message': f'Local machine contains Java version [{expected_java_version}].'}
        else:
            return {'passed': False, 'message': f'The installed java version is not correct.'}
    except Exception as e:
        print(e)
        return {'passed': False, 'message': f'Could not determine if Java was installed..'}


def description():
    return f'Validate Java version [{expected_java_version}] is installed.'
