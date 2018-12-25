"""
Missing Argument Exception
"""


class Missing_Argument(Exception):
    """Missing Argument Custom Exception"""

    def __init__(self, message, error_info={}):
        Exception.__init__(self, message)
        self.error_info = error_info
