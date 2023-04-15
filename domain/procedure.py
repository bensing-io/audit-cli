import hashlib
import os
import sys


class Procedure:
    def __init__(self, procedure_file):
        self.file = procedure_file
        self.was_executed = False
        self.is_valid = True
        self.invalid_message = ""
        self.passed = False
        self.message = ""
        self.description = None
        self.type = None

        try:
            self.file_name = os.path.basename(self.file)
            self.fingerprint = hashlib.sha256(open(self.file, 'rb').read()).hexdigest()
            module_name = os.path.splitext(os.path.basename(self.file))[0]
            sys.path.append(os.path.dirname(self.file))
            module = __import__(module_name)
            self.evaluate_method = getattr(module, 'evaluate')
            self.description_method = getattr(module, 'description')
            self.type_method = getattr(module, 'type')
            self.description = self.description_method()
            self.type = self.type_method()
        except Exception as e:
            self.is_valid = False
            self.invalid_message = str(e)

    def evaluate(self, file_path):
        result = {}
        try:
            outcome = self.evaluate_method(file_path)
            self.passed = outcome['passed']
            self.message = outcome["message"]
            self.was_executed = True
        except Exception as e:
            self.passed = False
            self.message = str(e)
            self.was_executed = False
        return result

