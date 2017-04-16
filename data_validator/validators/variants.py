from data_validator.validators.base import BaseValidator


class Variants(BaseValidator):
    def __init__(self, expected, case_sensitive=True, handler=None):
        self.case_sensitive = case_sensitive
        super().__init__(expected, handler)

    def validate(self, value):
        if not self.case_sensitive:
            self.expected = list(map(lambda x: x.lower(), self.expected))
            value = value.lower()
        if value not in self.expected:
            return value
