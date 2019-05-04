"""
Global Template Variables
"""

# Standard Library
import os

# Local Library
from app.modules.entity.option_entity import Option_Entity


def globals(request):

    option_entity = Option_Entity()

    return {
        "google_account": option_entity.get_value_by_key("google_analytics_account", ""),
        "app_timezone": os.getenv("APP_TIMEZONE", "UTC"),
    }
