"""
Health Check Command

see https://docs.djangoproject.com/en/2.0/howto/custom-management-commands/
"""

# Third Party Library
from django.core.management.base import BaseCommand, CommandError

# Local Library
from app.modules.core.health import Health


class Command(BaseCommand):

    help = "Health Check Silverback!"

    available = [
        "check"
    ]

    def add_arguments(self, parser):
        """Config Command Args"""
        parser.add_argument('command', type=str, nargs='+', help='Available commands are %s' % ", ".join(self.available))

    def handle(self, *args, **options):
        """Command Handle"""
        if len(options['command']) == 0 or options['command'][0] not in self.available:
            raise CommandError('Command Does not exist! Please use one of the following: python manage.py health [%s]' % ", ".join(self.available))

        command = options['command'][0]

        if command == "check":
            health = Health()
            status = Health.OK
            errors = []
            errors.extend(health.check_db())
            errors.extend(health.check_io())
            errors.extend(health.check_workers())

            if len(errors) > 0:
                status = Health.NOT_OK

            if status == Health.OK:
                print(Health.OK)
            else:
                raise Exception("%(status)s: %(errors)s" % {
                    "status": Health.NOT_OK,
                    "errors": ", ".join(errors)
                })
