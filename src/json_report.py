"""JSONReport converts the AuditReport into a JSON output
which is stored in a local directory"""


class JSONReport:
    """JSONReport converts the AuditReport into a JSON output
    which is stored in a local directory"""

    def __init__(self, audit):
        self.report = audit.get_report()

    def generate_report(self) -> {}:
        """Invoke to generate the JSON report"""

        target = {
            'file': self.report.target_file(),
            'fingerprint': self.report.target_file_fingerprint()
        }

        summary = {
            'outcome': self.report.outcome().value,
            'total': self.report.total(),
            'executed': self.report.executed(),
            'passed': self.report.passed(),
            'failed': self.report.failed(),
            'inconclusive': self.report.inconclusive()
        }

        standards = []
        for procedure_result in self.report.standards_details():
            standards.append({
                'description': procedure_result.description(),
                'outcome': procedure_result.outcome().value,
                'reason': procedure_result.message(),
                'file': procedure_result.file_name(),
                'fingerprint': procedure_result.file_fingerprint(),
            })

        guidelines = []
        for procedure_result in self.report.guidelines_details():
            guidelines.append({
                'description': procedure_result.description(),
                'outcome': procedure_result.outcome().value,
                'reason': procedure_result.message(),
                'file': procedure_result.file_name(),
                'fingerprint': procedure_result.file_fingerprint(),
            })

        details = {
            'standards': standards,
            'guidelines': guidelines
        }

        report = {
            'target': target,
            'summary': summary,
            'details': details
        }

        return report
