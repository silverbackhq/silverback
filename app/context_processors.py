"""
Global Template Variables
"""

# Standard Library
import os

# Local Library
from app.modules.entity.option_entity import OptionEntity
from app.modules.core.constants import Constants


def globals(request):

    option_entity = OptionEntity()

    return {
        "google_account": option_entity.get_value_by_key("google_analytics_account", ""),
        "app_timezone": os.getenv("APP_TIMEZONE", "UTC"),
        "activate_notifications": os.getenv("ACTIVATE_NOTIFICATIONS", "false") == "true",
        "constants": Constants(),
    }
