import json

min_pr_reviewers = 2


def evaluate(lines):
    pull_request = json.loads(''.join(lines))
    reviewers = pull_request['requested_reviewers']
    if len(reviewers) >= min_pr_reviewers:
        return {'passed': True, 'message': f'There are {len(reviewers)} PR Reviewers.'}
    else:
        return {'passed': False, 'message': f'There are only {len(reviewers)} PR Reviewers, '
                                            f'when there needs to be a minimum of {min_pr_reviewers} PR Reviewers.'}


def description():
    return f'There must be at least {min_pr_reviewers} PR reviewers.'
