"""CliTerminalReport converts the AuditReport into a terminal-frindly report"""

from audit_outcome import AuditOutcome


class CliTerminalReport:
    """CliTerminalReport converts the AuditReport into a terminal-frindly report"""

    def __init__(self, audit):
        self.report = audit.get_report()

    def generate_report(self):
        """Invoke to generate the terminal report"""

        self._print_summary()
        print()
        self._print_standards_details()
        print()
        self._print_guidelines_details()
        print()

    def _print_summary(self):
        print()
        self._print_summary_intro_row('Target File', f'\033[94m{self.report.target_file()}\033[0m')
        self._print_summary_intro_row('Outcome', self._outcome_indicator(self.report.outcome()))
        print('-' * 20)
        self._print_summary_data_row('Total', self.report.total())
        self._print_summary_data_row('Executed', self.report.executed())
        self._print_summary_data_row('Passed', self.report.passed())
        self._print_summary_data_row('Failed', self.report.failed())
        self._print_summary_data_row('Inconclusive', self.report.inconclusive())
        print('-' * 20)

    @staticmethod
    def _print_summary_data_row(title, value):
        print('{:<15} {:<5}'.format(f'{title}:', f'{value}'))

    @staticmethod
    def _print_summary_intro_row(title, value):
        print('{:<15} {:<100}'.format(f'{title}:', f'{value}'))

    def _print_standards_details(self):
        self._print_procedure_details_table('Standards', self.report.standards_details())

    def _print_guidelines_details(self):
        self._print_procedure_details_table('Guidelines', self.report.guidelines_details())

    def _print_procedure_details_table(self, table_name, procedures):
        print('{:<144}'.format(f'{table_name}'))
        print('-' * 20)
        if len(procedures) == 0:
            _no_procs = 'No Procedures Executed'
            print(f'\033[93m{_no_procs}\033[0m')
            return
        for procedure in procedures:
            outcome = self._outcome_indicator(procedure.outcome())
            print('{:<15} {:<15}'.format('Description:', procedure.description()))
            print('{:<15} {:<15}'.format('Outcome:', outcome))
            print('{:<15} {:<15}'.format('Reason:', procedure.message()))
            print()

    @staticmethod
    def _outcome_indicator(audit_outcome) -> str:
        outcome = ''
        if audit_outcome == AuditOutcome.PASSED:
            outcome = '\033[92mPassed\033[0m'
        elif audit_outcome == AuditOutcome.FAILED:
            outcome = '\033[91mFailed\033[0m'
        elif audit_outcome == AuditOutcome.INCONCLUSIVE:
            outcome = '\033[93mInconclusive\033[0m'
        elif audit_outcome == AuditOutcome.WARNING:
            outcome = '\033[93mWarning\033[0m'
        return outcome
