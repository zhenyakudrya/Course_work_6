from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='Zhenya20031997@yandex.ru',
            first_name='Admin',
            last_name='Adminovich',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )

        user.set_password('Skypro123')
        user.save()
