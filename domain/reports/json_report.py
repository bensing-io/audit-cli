class JSONReport:

    def __init__(self, audit):
        self.report = audit.get_report()

    def generate_report(self) -> {}:
        target = {
            'file': self.report.target_file(),
            'fingerprint': self.report.target_file_fingerprint()
        }

        summary = {
            'total': self.report.total(),
            'executed': self.report.executed(),
            'passed': self.report.passed(),
            'failed': self.report.failed(),
        }

        standards = []
        for procedure_result in self.report.standards_details():
            standards.append({
                'description': procedure_result.description(),
                'outcome': procedure_result.outcome().value,
                'message': procedure_result.message(),
                'file': procedure_result.file_name(),
                'fingerprint': procedure_result.file_fingerprint(),
            })

        guidelines = []
        for procedure_result in self.report.guidelines_details():
            guidelines.append({
                'description': procedure_result.description(),
                'outcome': procedure_result.outcome().value,
                'message': procedure_result.message(),
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
