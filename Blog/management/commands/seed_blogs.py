from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from Blog.models import Blog_table
from django.utils import timezone
import random

# lightweight built-in lorem helpers to avoid external dependency
SAMPLE_SENTENCES = [
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit',
    'Praesent commodo cursus magna, vel scelerisque nisl consectetur et',
    'Donec id elit non mi porta gravida at eget metus',
    'Cras mattis consectetur purus sit amet fermentum',
    'Aenean lacinia bibendum nulla sed consectetur',
    'Integer posuere erat a ante venenatis dapibus posuere velit aliquet',
    'Etiam porta sem malesuada magna mollis euismod',
    'Nullam id dolor id nibh ultricies vehicula ut id elit',
    'Maecenas faucibus mollis interdum',
    'Sed posuere consectetur est at lobortis',
    'Curabitur blandit tempus porttitor',
    'Vestibulum id ligula porta felis euismod semper',
]

def _fake_sentence():
    # return a sentence with a period at the end
    return random.choice(SAMPLE_SENTENCES) + '.'

def _fake_paragraph():
    # paragraph made of 3-7 sentences
    return ' '.join(_fake_sentence() for _ in range(random.randint(3, 7)))


class Command(BaseCommand):
    help = 'Seed the Blog_table with fake blog records.'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=50, help='Number of blog records to create')
        parser.add_argument('--username', type=str, default=None, help='Username of the owner user to attach blogs to')
        parser.add_argument('--email', type=str, default=None, help='Email to create/find user')
        parser.add_argument('--password', type=str, default='password123', help='Password for created user (if any)')

    def handle(self, *args, **options):
        User = get_user_model()
        count = options['count'] or 50
        username = options.get('username')
        email = options.get('email')
        password = options.get('password') or 'password123'

        # ensure owner user exists
        if username:
            user, created = User.objects.get_or_create(username=username, defaults={'email': email or f'{username}@example.com'})
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created user "{username}"'))
        elif email:
            user, created = User.objects.get_or_create(email=email, defaults={'username': email})
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created user with email "{email}"'))
        else:
            # fallback to first user in DB or create a test user
            user = User.objects.first()
            if not user:
                user = User.objects.create_user(username='seed_user', email='seed_user@example.com', password=password)
                self.stdout.write(self.style.SUCCESS('Created fallback user "seed_user"'))

        titles = [
            'How to build a Django app',
            'Tips for writing clean code',
            'Deploying to production',
            'Understanding Python internals',
            'Async in Django',
            'Testing strategies',
            'API design best practices',
        ]

        created_count = 0
        for i in range(count):
            title = random.choice(titles) + ' — ' + _fake_sentence().rstrip('.')
            description = '\n\n'.join([_fake_paragraph() for _ in range(random.randint(1, 3))])
            # Image field can remain default (empty string) or point to a placeholder
            blog = Blog_table.objects.create(
                user_id=user,
                title=title[:150],
                Description=description,
                date=timezone.now(),
            )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Created {created_count} Blog_table records attached to user "{user.username}"'))
