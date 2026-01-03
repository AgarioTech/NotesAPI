import pytest
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.users.models import CustomUser


@pytest.mark.django_db
class TestNoteInteractions:
    def setup_method(self):
        self.user = CustomUser.objects.create_user(
            username='TestUser',
            email='test@gmail.com',
            password='O2d6sh8vv4'
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access = str(self.refresh.access_token)
        self.headers = {
            'HTTP_AUTHORIZATION': f'Bearer {self.access}'
        }

        self.second_user = CustomUser.objects.create_user(
            username='secondTestUser',
            email='secondtest@gmail.com',
            password='O2d6sh8vv4'
        )
        self.second_refresh = RefreshToken.for_user(self.second_user)
        self.second_access = str(self.second_refresh.access_token)
        self.second_headers = {
            'HTTP_AUTHORIZATION': f'Bearer {self.second_access}'
        }
        self.url = 'http://127.0.0.1:8000/api/v1/users/'

    def test_user_get_all(self, client):
        request = client.get(f'{self.url}')
        response = request.json()
        assert response['count'] == 2
        assert request.status_code == 200

    def test_user_get_one(self, client):
        request = client.get(f'{self.url}{self.user.id}/')
        response = request.json()
        assert response['username'] == self.user.username
        assert request.status_code == 200

    def test_user_get_one_404(self, client):
        request = client.get(f'{self.url}999/')
        response = request.json()
        assert response['detail'] == 'No CustomUser matches the given query.'
        assert request.status_code == 404

    # request create user
    def test_user_post(self, client):
        request = client.post(f'{self.url}', data={
            "username": "test_username",
            "password": "O2d6sh8vv4",
            "email": "testemail@gmail.com"
        })
        response = request.json()
        assert response['username'] == 'test_username'
        assert request.status_code == 201

    def test_user_post_400(self, client):
        request = client.post(f'{self.url}', data={
            "username": "test_username",
            "password": "O2d6sh8vv4",
        })
        response = request.json()
        assert response['email'] == ['This field is required.']
        assert request.status_code == 400

    def test_user_partial_update(self, client):
        request = client.patch(f'{self.url}{self.user.id}/', **self.headers, data={
            "username": "TestUser",
        },
        content_type='application/json')
        assert request.status_code == 200

    def test_user_partial_update_401(self, client):
        request = client.patch(f'{self.url}{self.user.id}/', data={
            "username": "TestUser",
        },
        content_type='application/json')
        response = request.json()
        assert response['detail'] == 'Authentication credentials were not provided.'
        assert request.status_code == 401

    def test_user_partial_update_403(self, client):
        request = client.patch(f'{self.url}{self.user.id}/', **self.second_headers, data={
            "username": "TestUser",
        },
        content_type='application/json')
        response = request.json()
        assert response['detail'] == 'You do not have permission to perform this action.'
        assert request.status_code == 403

    def test_user_partial_update_404(self, client):
        request = client.patch(f'{self.url}999/', **self.headers, data={
            "username": "TestUser"
        },
        content_type='application/json')
        response = request.json()
        assert response['detail'] == 'No CustomUser matches the given query.'
        assert request.status_code == 404

    def test_user_update(self, client):
        request = client.put(f'{self.url}{self.user.id}/', **self.headers, data={
            "username": "TestUser",
            "password": "O2d6sh8vv4",
            "email": "test@gmail.com"
        },
        content_type='application/json')
        assert request.status_code == 200

    def test_user_update_401(self, client):
        request = client.put(f'{self.url}{self.user.id}/', data={
            "username": "TestUser",
            "password": "O2d6sh8vv4",
            "email": "test@gmail.com"
        },
        content_type='application/json')
        response = request.json()
        assert response['detail'] == 'Authentication credentials were not provided.'
        assert request.status_code == 401

    def test_user_update_403(self, client):
        request = client.put(f'{self.url}{self.user.id}/', **self.second_headers, data={
            "username": "TestUser",
            "password": "O2d6sh8vv4",
            "email": "test@gmail.com"
        },
        content_type='application/json')
        response = request.json()
        assert response['detail'] == 'You do not have permission to perform this action.'
        assert request.status_code == 403

    def test_user_update_404(self, client):
        request = client.put(f'{self.url}999/', **self.headers, data={
            "username": "TestUser",
            "password": "O2d6sh8vv4",
            "email": "test@gmail.com"
        },
        content_type='application/json')
        response = request.json()
        assert response['detail'] == 'No CustomUser matches the given query.'
        assert request.status_code == 404

    def test_user_destroy(self, client):
        request = client.delete(f'{self.url}{self.user.id}/', **self.headers,
        content_type='application/json')
        assert request.status_code == 204

    def test_user_destroy_401(self, client):
        request = client.delete(f'{self.url}{self.user.id}/',content_type='application/json')
        response = request.json()
        assert response['detail'] == 'Authentication credentials were not provided.'
        assert request.status_code == 401

    def test_user_destroy_403(self, client):
        request = client.delete(f'{self.url}{self.user.id}/', **self.second_headers,
        content_type='application/json')
        response = request.json()
        assert response['detail'] == 'You do not have permission to perform this action.'
        assert request.status_code == 403


    def test_user_login(self, client):
        request = client.post(f'{self.url}login/', data={
            "username": "TestUser",
            "password": "O2d6sh8vv4"
        })
        assert request.status_code == 200

    def test_user_login_400(self, client):
        request = client.post(f'{self.url}login/', data={
            "username": "TestUser",
        })
        response = request.json()
        assert response['error'] == 'Invalid credentials'
        assert request.status_code == 400

    def test_user_login_404(self, client):
        request = client.post(f'{self.url}login/', data={
            "username": "NotFoundUser",
            "password": "invalid_password"
        })
        response = request.json()
        assert response['detail'] == 'No CustomUser matches the given query.'
        assert request.status_code == 404