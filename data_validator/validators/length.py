from data_validator.validators.base import BaseValidator


class StringLength(BaseValidator):
    min = None
    max = None

    def __init__(self, expected, handler=None):
        """
        
        :param expected: Expected range. Example: [1,10]
        :type expected: list | tuple  
        :param handler: Function to change value if value is unexpected
        """
        super().__init__(expected, handler)
        self.min, self.max = expected[0], expected[1]

    def validate(self, value):
        length = len(value)
        if length < self.min or length > self.max:
            return length
