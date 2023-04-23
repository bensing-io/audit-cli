import hashlib
import os
import sys

from audit_outcome import AuditOutcome


class Procedure:
    def __init__(self, procedure_file):
        self.file = procedure_file
        self.is_valid = False
        self.invalid_message = ""
        self.was_executed = False
        self.outcome = "fail"
        self.message = ""
        self.description = ""
        self.type = ""

        try:
            self.file_name = os.path.basename(self.file)
            self.fingerprint = hashlib.sha256(open(self.file, 'rb').read()).hexdigest()
            module_name = os.path.splitext(os.path.basename(self.file))[0]
            sys.path.append(os.path.dirname(self.file))
            module = __import__(module_name)
            self.evaluate_method = getattr(module, 'evaluate')
            self.description_method = getattr(module, 'description')
            self.type_method = getattr(module, 'procedure_type')
            self.description = self.description_method()
            self.type = self.type_method()
            self.is_valid = True
        except Exception as e:
            self.is_valid = False
            self.invalid_message = str(e)

    def evaluate(self, file_path):
        result = {}
        try:
            _outcome, _message = self.evaluate_method(file_path)
            self.outcome = AuditOutcome.validate(_outcome)
            self.message = _message
            self.was_executed = True
        except Exception as e:
            self.outcome = AuditOutcome.Inconclusive
            self.message = str(e)
            self.was_executed = False
        return result
