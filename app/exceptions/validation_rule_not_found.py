"""
Validation Rule Not Found
"""


class Validation_Rule_Not_Found(Exception):
    """Validation Rule Not Exist Custom Exception"""

    def __init__(self, error_info):
        Exception.__init__(self, "Validation Rule Not Found!")
        self.error_info = error_info
