import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from datetime import datetime
from accounts.models import User

@pytest.fixture
def api_clinet():
    client = APIClient()
    return  client

@pytest.fixture
def common_user():
    user = User.objects.create_user(email='admim@a.admincom', password='241195cna', is_verified=True)
    return user


@pytest.mark.django_db
class TestPostApi:

    def test_get_post_response_200(self, api_clinet):
        url = reverse('blog:api-v1:post-list')
        response = api_clinet.get(url)
        assert response.status_code == 200

    # def test_create_post_response_201(self,api_clinet,common_user):
    #     url = reverse('blog:api-v1:post-list')
    #     data = {
    #         'title': 'test',
    #         'content': 'description',
    #         'status': True,
    #         'published_date': datetime.now()
    #     }
    #     user=common_user
    #     api_clinet.force_authenticate(user=user)
    #     response = api_clinet.post(url,data)
    #     assert response.status_code == 201

    def test_create_post_invalid_data_response_201(self, api_clinet, common_user):
        url = reverse('blog:api-v1:post-list')
        data = {

            'content': 'description',
            'status': True,
            'published_date': datetime.now()
        }
        user = common_user
        api_clinet.force_authenticate(user=user)
        response = api_clinet.post(url, data)
        assert response.status_code == 400
