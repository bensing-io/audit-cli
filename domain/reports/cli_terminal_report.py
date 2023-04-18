from domain.audit_outcome import AuditOutcome


class CliTerminalReport:

    def __init__(self, audit):
        self.report = audit.get_report()

    def generate_report(self):
        self._print_summary()
        print("\n")
        self._print_standards_details()
        print("\n")
        self._print_guidelines_details()
        print("\n")

    def _print_summary(self):
        pass_fail_indicator = '\033[91m Failed \033[0m' if not self.report.outcome() == AuditOutcome.Passed \
            else '\033[92m Passed \033[0m'
        print("\n")
        print(f'Summary - {pass_fail_indicator}')
        print('-' * 20)
        print(f'Target File: {self.report.target_file()}')
        print('-' * 20)
        print(f'Total:\t{self.report.total()}')
        print(f'Exec:\t{self.report.executed()}')
        print(f'Pass:\t{self.report.passed()}')
        print(f'Fail:\t{self.report.failed()}')
        print('-' * 20)

    def _print_standards_details(self):
        self._print_procedure_details_table('Standards',self.report.standards_details())

    def _print_guidelines_details(self):
        self._print_procedure_details_table('Guidelines', self.report.guidelines_details())

    @staticmethod
    def _print_procedure_details_table(table_name, procedures):
        print('{:<60} {:<10} {:<60}'.format(f'{table_name}', 'Outcome', 'Message'))
        print('-' * 20)
        for procedure in procedures:
            outcome = '\033[92m pass \033[0m' if procedure.outcome() == AuditOutcome.Passed \
                else '\033[91m fail \033[0m'
            print(f'{procedure.description():<60} {outcome:<10} {procedure.message():<60}')