from django.core.management.base import BaseCommand, CommandError
from auth_by_email.models import DjGrammUserManager, DjGrammUser


class Command(BaseCommand):
    help = 'Creates user with email and default password ' \
           'without email verification'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str)

    def handle(self, *args, **options):
        password = 'password'
        try:
            manager = DjGrammUserManager()
            manager.model = DjGrammUser
            user = manager._create_user(email=options['email'],  # noqa
                                        password=password,
                                        is_active=True
                                        )
        except ValueError as e:
            raise CommandError(e.message) # noqa

        user.save()
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created user: "{user.email}"'
                               f' with password: "{password}"')
        )
