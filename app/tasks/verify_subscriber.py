"""
Verify Subscriber Tasks
"""

# Third Party Library
from celery import shared_task

# Local Library
from app.modules.entity.option_entity import OptionEntity
from app.modules.core.subscriber import Subscriber as SubscriberModule


@shared_task
def verify_subscriber(subscriber_id):

    # option_entity = OptionEntity()
    subscriber_module = SubscriberModule()

    # app_name = option_entity.get_value_by_key("app_name")
    # app_email = option_entity.get_value_by_key("app_email")
    # app_url = option_entity.get_value_by_key("app_url")
    subscriber = subscriber_module.get_one_by_id(subscriber_id)

    if not subscriber:
        return {
            "status": "passed",
            "result": "{}"
        }

    if subscriber.type == SubscriberModule.EMAIL:
        result = __verify_email()
    elif subscriber.type == SubscriberModule.PHONE:
        result = __verify_phone()
    elif subscriber.type == SubscriberModule.ENDPOINT:
        result = __verify_endpoint()

    return result


@shared_task
def __verify_email():
    pass


@shared_task
def __verify_phone(to, ):
    pass


@shared_task
def __verify_endpoint():
    pass
