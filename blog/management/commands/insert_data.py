from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User, Profile
from blog.models import Post, Category
from datetime import datetime
import random

category_list = [
    'IT',
    'Design',
    'DevOps'
]

class Command(BaseCommand):
    help = 'Inserting fake data'

    def __init__(self):
        self.fake = Faker()

    def handle(self, *args, **options):
        user = User.objects.create_user(email=self.fake.email(), password='test@123', is_active=False)
        profile = Profile.objects.get(user=user)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.description = self.fake.paragraph(nb_sentences=5)
        profile.save()

        for name in category_list:
            Category.objects.get_or_create(name = name)

        for _ in range(10):
            Post.objects.create(
                author=profile,
                title=self.fake.paragraph(nb_sentences=1),
                content=self.fake.paragraph(nb_sentences=6),
                status=random.choice([True, False]),
                published_date=datetime.now(),
                category=Category.objects.get(name= random.choice(category_list))
            )