from django.test import TestCase
from ..models import Post, Category
from datetime import datetime

from accounts.models import User, Profile

class TestPostModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='test2@test.com', password='123')
        self.profile = Profile.objects.create(
            user=self.user,
            first_name='test-name',
            last_name='last-name',
            description='test, d'
        )

    def test_create_post_with_valid_data(self):
        post = Post.objects.create(
            author= self.profile,
            title= 'test',
            content= 'description',
            status= True,
            category= None,
            published_date= datetime.now()
        )
        self.assertTrue(Post.objects.filter(pk=post.id).exists())