"""
    Validation Rule Not Found
    ~~~~~~~~~~~~~~

    :copyright: silverbackhq
    :license: BSD-3-Clause
"""


class ValidationRuleNotFound(Exception):
    """Validation Rule Not Exist Custom Exception"""

    def __init__(self, error_info):
        Exception.__init__(self, "Validation Rule Not Found!")
        self.error_info = error_info
