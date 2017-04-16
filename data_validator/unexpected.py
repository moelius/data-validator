class Unexpected:
    __slots__ = ["value", "validator", "expected", "unexpected", "path"]

    def __init__(self, value, validator, expected, unexpected, path=None):
        self.value = value
        self.validator = validator
        self.expected = expected
        self.unexpected = unexpected
        self.path = path

    def __str__(self):
        return '%svalue: %s, validator: %s, expected: %s, unexpected: %s' % (
            'path: %s, ' % '.'.join([str(path) for path in self.path]) or '',
            self.value, self.validator, self.expected, self.unexpected)

    def as_dict(self):
        return dict(path=self.path, value=self.value, validator=self.validator, expected=self.expected,
                    unexpected=self.unexpected)
