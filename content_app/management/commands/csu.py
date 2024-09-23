from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Команда для создания суперпользователя"""

    def handle(self, *args, **options):
        user = User.objects.create(
            email='django292@gmail.com',
            phone='89111720292',
            first_name='django0292',
            is_active=True,
            is_staff=True,
            is_superuser=True
        )

        user.set_password('2920')
        user.save()
