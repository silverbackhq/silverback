"""
    Sanitization Rule Not Found
    ~~~~~~~~~~~~~~

    :copyright: silverbackhq
    :license: BSD-3-Clause
"""


class SanitizationRuleNotFound(Exception):
    """Sanitization Rule Not Exist Custom Exception"""

    def __init__(self, error_info):
        Exception.__init__(self, "Sanitization Rule Not Found!")
        self.error_info = error_info
