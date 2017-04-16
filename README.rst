==============
Data-validator
==============

Validator with feature to change unexpected values.

Features
--------

- recursive validation dictionary values
- expanding the list of validators with custom validators
- ability to assign handler functions globally or on single validator to change unexpected values
- ability to throw exceptions on first error or after complete validation process
- ability to return unexpected results and info about them

Installation
------------

As usually use pip:

.. code-block:: bash

    pip install data-validator

Usage examples
--------------

Basic dictionary validation:

.. code-block:: python

    # user to validate
    user = {
        'first_name': 'Very long name to validate',
        'last_name': 'Smith',
        'email': 'smith@gmail.com',
        'second_email': 'bad email',
        'address': {'state': 'Texas', 'city': 'Dallas'},
        'career': [{'name': 'google', 'from': 2012, 'until': 'now'}, {'name': 'facebook', 'from': -1,
                    'until': 44444444444444}]
    }

    # We want to validate:
    # user['first_name'] and user['last_name'] length must be more then 2 and less then 10
    # user['email'] and user['second_email'] must match regex pattern r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$"
    # user['address']['state'] may be Texas, Alabama or Alaska and it case sensitive
    # user['address']['city'] may be New York, Los Angeles or Washington and it not case sensitive
    # user['career'][*]['from'] and user['career'][*]['until'] must be int16. P.s. * is list index

    # And if we have unexpected values we need to change them with handler function - lambda x: -1
    # and if user['career']['until'] is unexpected we need to change this with handler function - lambda x: -2

    # user validation rules
    rules = {
        'first_name': [validators.StringLength([2, 10])],
        'last_name': [validators.StringLength([2, 10])],
        'email': [validators.Regex(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$")],
        'second_email': [validators.Regex(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$")],
        'address.state': [validators.Variants(['Texas', 'Alabama', 'Alaska'])],
        'address.city': [validators.Variants(['New York', 'Los Angeles','Washington'], case_sensitive=False)],
        'career.from': [validators.IntNumberType(numpy.int16)],
        'career.until': [validators.IntNumberType(numpy.int16, handler=lambda x: -2)]
    }

    # validate user
    validator = Validator(rules, common_handler=lambda x: -1)
    validator_result = validator.validate(user)
    if not validator_result:
        [print(unexpected) for unexpected in validator.unexpected_values]

    # result will be
    # path: career.0.until, value: now, validator: <data_validator.validators.types.IntNumberType object at 0x7ffada681af8>, expected: <class 'numpy.int16'>, unexpected: <class 'str'>
    # path: career.1.until, value: 2015555555, validator: <data_validator.validators.types.IntNumberType object at 0x7ffada681af8>, expected: <class 'numpy.int16'>, unexpected: <class 'numpy.int32'>
    # path: address.city, value: Dallas, validator: <data_validator.validators.variants.Variants object at 0x7ffada681a68>, expected: ['new york', 'los angeles'], unexpected: dallas
    # path: second_email, value: bad email, validator: <data_validator.validators.regex.Regex object at 0x7ffada6819d8>, expected: ^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$, unexpected: bad email
    # path: first_name, value: Very long name to validate, validator: <data_validator.validators.length.StringLength object at 0x7ffada6c7120>, expected: [2, 10], unexpected: 26

    # We can find original item in validator.original_item and changed dict in validator.processed_item:
    {
        'first_name': -1,
        'last_name': 'Smith',
        'email': 'smith@gmail.com',
        'second_email': -1,
        'address': {'state': 'Texas', 'city': -1},
        'career': [{'name': 'google', 'from': -1, 'until': -2}, {'name': 'facebook', 'from': -1, 'until': -2}]
    }


