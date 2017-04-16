from copy import deepcopy

from data_validator.exceptions import ValidatorException
from data_validator.unexpected import Unexpected
from data_validator.validators.base import BaseValidator


class Validator:
    __slots__ = ["_rules", "_unexpected_values", "_common_handler", "_splitter", "_validate_value",
                 "_process_path", "original_item", "processed_item", "throw_exception", "break_on_first_error"]

    def __init__(self, rules, splitter='.', common_handler=None, throw_exception=False, break_on_first_error=False):
        """

        :param rules: Validation rules 
        :param splitter: Custom items path splitter
        :type splitter: str
        :param common_handler: Function to change value if value is unexpected
        :param throw_exception: If True exception will be thrown
        :type throw_exception: bool
        :param break_on_first_error: If True validation process will stop after first error 
        :type break_on_first_error: bool
        """
        self._rules = rules
        self._common_handler = common_handler
        self._splitter = splitter
        self._unexpected_values = None
        self.original_item = None
        self.processed_item = None
        self._process_path = None
        self.throw_exception = throw_exception
        self.break_on_first_error = break_on_first_error

    def validate(self, item):
        """
        
        :param item: item to validate 
        :return: 
        """
        self._unexpected_values = []
        self.original_item = item
        self.processed_item = deepcopy(self.original_item)
        for str_path, validators in self.validation_rules.items():
            self._process_path = []
            path_list = str_path.split(self._splitter)
            self._rec_validate(self.original_item, validators, path_list)
            if self.break_on_first_error:
                break
        if self.throw_exception:
            raise ValidatorException(message='Validator error', errors=self.unexpected_values)
        return False if self.unexpected_values else True

    def _rec_validate(self, item, validate_rules, path_list):
        if isinstance(item, list):
            temp_path = self._process_path[:]
            for index, item_part in enumerate(item):
                self._process_path = temp_path[:]
                self._process_path.append(index)
                temp_path_list = path_list[:]
                self._rec_validate(item=item_part, validate_rules=validate_rules, path_list=temp_path_list)
        else:
            path = path_list.pop(0)
            if path not in item or not item[path]:
                return
            if path_list:
                self._process_path.append(path)
                self._rec_validate(item=item[path], validate_rules=validate_rules, path_list=path_list)
            else:
                self._process_path.append(path)
                validate_value = item[path]
                unexpected_list = self.validate_value(validate_value, validate_rules, throw_exception=False,
                                                      break_on_first_error=False, path=self._process_path)
                if unexpected_list and not isinstance(unexpected_list, bool):
                    self.unexpected_values.extend(unexpected_list)
                    for unexpected in unexpected_list:
                        if unexpected.validator.handler:
                            self._update_unexpected(self.processed_item, self._process_path,
                                                    unexpected.validator.handler(validate_value))
                        elif self._common_handler:
                            self._update_unexpected(self.processed_item, self._process_path,
                                                    self._common_handler(validate_value))

    @staticmethod
    def validate_value(value, validators, throw_exception=False, break_on_first_error=False, **kwargs):
        """

        :param value: Value to validate
        :param validators: list of Validators objects
        :type validators: list of BaseValidator
        :param throw_exception: If True exception will be thrown
        :type throw_exception: bool
        :param break_on_first_error: If True validation process will stop after first error 
        :type break_on_first_error: bool
        :return: 
        """
        unexpected_values = []
        for validator_obj in validators:
            unexpected = validator_obj.validate(value)
            if unexpected:
                unexpected_values.append(
                    Unexpected(value=value, validator=validator_obj,
                               expected=validator_obj.expected, unexpected=unexpected,
                               path=kwargs['path'] if 'path' in kwargs else None))
            if break_on_first_error:
                break
        if throw_exception:
            raise ValidatorException(message='Validator error', errors=unexpected_values)

        return unexpected_values or True

    @staticmethod
    def _update_unexpected(d, p, v):
        """

        :param d: Dictionary to update 
        :type d: dict
        :param p: Path of value to update
        :type p: list
        :param v: 
        :return: 
        """
        if len(p) == 1:
            d[p[0]] = v
        else:
            Validator._update_unexpected(d[p[0]], p[1:], v)

    @property
    def validation_rules(self):
        return self._rules

    @property
    def unexpected_values(self):
        return self._unexpected_values
