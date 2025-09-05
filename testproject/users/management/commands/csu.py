from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(username="admin")
        user.set_password("12345")
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
