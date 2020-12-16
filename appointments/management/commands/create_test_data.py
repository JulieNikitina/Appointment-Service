from django.core.management.base import BaseCommand
from appointments.models import User, Doctor


class Command(BaseCommand):
    help = 'Creates test data'

    def handle(self, *args, **options):
        User.objects.create_superuser(
            username='admin',
            password='admin'
        )

        User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        doctors = [
            ('Gregory', 'House', 'pediatrician'),
            ('James', 'Wilson', 'oncologist'),
            ('Eric', 'Foreman', 'diagnostician'),
            ('Robert', 'Chase', 'surgeon'),
            ('Allison', 'Cameron', 'diagnostician')
        ]

        for first_name, last_name, speciality in doctors:
            Doctor.objects.create(
                first_name=first_name,
                last_name=last_name,
                speciality=speciality
            )

        msg = self.style.SUCCESS('Done!')
        self.stdout.write(msg)
