from django.core.management.base import BaseCommand
from django.conf import settings
from leave.models import EmployeeProfile

class Command(BaseCommand):
    help = 'Eksik profilleri oluşturur.'

    def handle(self, *args, **kwargs):
        User = settings.AUTH_USER_MODEL
        users = User.objects.all()
        created_count = 0

        for user in users:
            if not hasattr(user, 'profile'):
                EmployeeProfile.objects.create(user=user)
                created_count += 1
        
        
        self.stdout.write(f"Profil oluşturuldu: {user.username}")

