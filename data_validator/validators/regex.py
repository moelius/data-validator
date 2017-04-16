import re

from data_validator.validators.base import BaseValidator


class Regex(BaseValidator):
    def __init__(self, expected, handler=None):
        """
        
        :param expected: regex pattern 
        """
        super().__init__(expected=expected, handler=handler)

    def validate(self, value):
        if not re.match(self.expected, value):
            return value
