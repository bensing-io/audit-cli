weight_max = 80


def description():
    return f'No given route can have more than {weight_max}% of traffic going to it for the service mesh'


def procedure_type():
    return "standard"


def evaluate(lines):
    weight = None
    for line in lines:
        if 'weight' in line:
            weight = int(line.split(': ')[1])
            break
    if weight and weight > 80:
        return {'outcome': 'failed', 'message': f'The weight from the route must be less than {weight_max}%. '
                                                f'Currently, the weight is {weight}%'}
    else:
        return {'outcome': 'passed', 'message': f'The weight from the route is '
                                            f'less than {weight_max}% at {weight}%.'}
