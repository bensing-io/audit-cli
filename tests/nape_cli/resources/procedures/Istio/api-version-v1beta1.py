expected_api_version = "networking.istio.io/v1beta1"


def description():
    return f'All service mesh kubernetes resources can only be API Version [{expected_api_version}]'


def procedure_type():
    return "standard"


def evaluate(lines):
    version = ""
    for line in lines:
        if line.strip().startswith('apiVersion:'):
            version = line.strip().split(':')[1].strip()
            break
    if version == expected_api_version:
        return 'passed', f'The API Version is properly set at [{expected_api_version}].'
    else:
        return 'failed', f'The API version must be [{expected_api_version}]. It is currently [{version}]'
