from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Division

User = get_user_model()


class Command(BaseCommand):
    help = 'Create the default Super Admin user for Al-Kawthar ERP'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='superadmin', help='Username (default: superadmin)')
        parser.add_argument('--email',    default='admin@alkawthar.edu.sa', help='Email address')
        parser.add_argument('--password', default='Admin@1234', help='Password')
        parser.add_argument('--fullname', default='System Administrator', help='Full name')

    def handle(self, *args, **options):
        username  = options['username']
        email     = options['email']
        password  = options['password']
        full_name = options['fullname']

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists.'))
            return

        # Ensure at least one division exists
        division, _ = Division.objects.get_or_create(
            name='AMERICAN',
            defaults={'description': 'American Division'}
        )

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            full_name=full_name,
            division=division,
        )
        self.stdout.write(self.style.SUCCESS(
            f'Super Admin "{user.username}" created successfully.\n'
            f'  Email   : {user.email}\n'
            f'  Password: {password}\n'
            f'  Role    : {user.get_role_display()}'
        ))
