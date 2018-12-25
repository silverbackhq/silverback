"""
Sanitization Rule Not Found
"""


class Sanitization_Rule_Not_Found(Exception):
    """Sanitization Rule Not Exist Custom Exception"""

    def __init__(self, error_info):
        Exception.__init__(self, "Sanitization Rule Not Found!")
        self.error_info = error_info
