from abc import ABCMeta, abstractmethod


class BaseValidator:
    __metaclass__ = ABCMeta
    __slots__ = ["expected", "handler"]

    @abstractmethod
    def __init__(self, expected, handler=None):
        """
        
        :param expected: Value to validate
        :param handler: Function to change value if value is unexpected
        """
        self.expected = expected or None
        self.handler = handler or None

    @abstractmethod
    def validate(self, *args, **kwargs):
        """Validate method
        
        :param args: 
        :param kwargs: 
        :return: 
        """
