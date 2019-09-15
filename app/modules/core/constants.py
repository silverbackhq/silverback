"""
Constants Module
"""


class Constants():

    INCIDENT_UPDATE_STATUSES = {
        "investigating": "Investigating",
        "identified": "Identified",
        "monitoring": "Monitoring",
        "update": "Update",
        "resolved": "Resolved",
    }

    COMPONENT_STATUSES = {
        "operational": "Operational",
        "degraded_performance": "Degraded Performance",
        "partial_outage": "Partial Outage",
        "major_outage": "Major Outage",
        "maintenance": "Maintenance",
    }
