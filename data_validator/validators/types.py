import numpy

from data_validator.validators.base import BaseValidator


class BaseType(BaseValidator):
    def __init__(self, expected, handler=None):
        super().__init__(expected=expected, handler=handler)

    def validate(self, value):
        if not isinstance(value, self.expected):
            return type(value)


class IntNumberType(BaseValidator):
    def __init__(self, expected, handler=None):
        """
        
        :param expected: Expected numpy int type. Example: numpy.int8 
        :param handler: 
        """
        super().__init__(expected=expected, handler=handler)

    def validate(self, value):
        try:
            r = self.expected(value)
            if r == value:
                return
        except OverflowError:
            pass
        except Exception:
            return type(value)
        n_types = (numpy.int8, numpy.int16, numpy.int32, numpy.int64, numpy.uint64)

        def _validate(value, max):
            return True if value <= max else False

        for n_type in n_types:
            if n_type == self.expected:
                continue
            max = numpy.iinfo(n_type).max
            if _validate(value, max):
                return n_type
        return type(value)
