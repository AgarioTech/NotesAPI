import pytest
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.notes.models import Note
from api.v1.users.models import CustomUser


# Create your tests here.
@pytest.mark.django_db
class TestNoteInteractions:
    def setup_method(self):
        self.user = CustomUser.objects.create_user(
            username='TestUser',
            email='test@gmail.com',
            password='O2d6sh8vv4'
        )
        self.user2 = CustomUser.objects.create_user(
            username='TestUser2',
            email='test2@gmail.com',
            password='O2d6sh8vv4'
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.refresh2 = RefreshToken.for_user(self.user2)
        self.access2 = str(self.refresh2.access_token)
        self.access = str(self.refresh.access_token)
        self.note = Note.objects.create(
            title='note_title',
            description='note_description',
            user=self.user
        )
        self.note2 = Note.objects.create(
            title='note_title2',
            description='note_description2',
            user=self.user2
        )
        self.note_data = {
            'title': 'note_title',
            'description': 'note_description',
        }
        self.headers = {
            'HTTP_AUTHORIZATION': f'Bearer {self.access}'
        }
        self.headers2 = {
            'HTTP_AUTHORIZATION': f'Bearer {self.access2}'
        }
        self.url = 'http://127.0.0.1:8000/api/v1/notes/'

    def test_note_partial_update(self, client):
        request = client.patch(f'http://127.0.0.1:8000/api/v1/notes/1/', **self.headers, data={
            'title': 'new_title'
        },
        content_type='application/json')
        assert request.status_code == 200

    def test_note_partial_update_401(self, client):
        request = client.patch(f'{self.url}{self.note.id}/', data=self.note_data,
        content_type='application/json')
        response = request.json()
        assert response['detail'] == 'Authentication credentials were not provided.'
        assert request.status_code == 401

    def test_note_partial_update_403(self, client):
        request = client.patch(f'{self.url}{self.note.id}/', **self.headers2, data=self.note_data,
        content_type='application/json')
        response = request.json()
        assert response['detail'] == 'You do not have permission to perform this action.'
        assert request.status_code == 403

    def test_note_partial_update_404(self, client):
        request = client.patch(f'{self.url}999/', **self.headers, data=self.note_data,
        content_type='application/json')
        response = request.json()
        assert response['detail'] == 'No Note matches the given query.'
        assert request.status_code == 404

    def test_note_update(self, client):
        request = client.put(f'{self.url}{self.note.id}/', **self.headers, data=self.note_data,
        content_type='application/json')
        assert request.status_code == 200

    def test_note_update_401(self, client):
        request = client.put(f'{self.url}{self.note.id}/', data=self.note_data,
        content_type='application/json')
        response = request.json()
        assert response['detail'] == 'Authentication credentials were not provided.'
        assert request.status_code == 401

    def test_note_update_403(self, client):
        request = client.put(f'{self.url}{self.note.id}/', **self.headers2, data=self.note_data,
        content_type='application/json')
        response = request.json()
        assert response['detail'] == 'You do not have permission to perform this action.'
        assert request.status_code == 403

    def test_note_update_404(self, client):
        request = client.put(f'{self.url}999/', **self.headers, data=self.note_data,
        content_type='application/json')
        response = request.json()
        assert response['detail'] == 'No Note matches the given query.'
        assert request.status_code == 404

    def test_note_post(self, client):
        request = client.post(f'{self.url}', **self.headers, data={
            'title': 'test_title',
            'description': 'test_description',
            'user': self.user.id,
        })
        response = request.json()
        assert response['user'] == self.user.id
        assert response['title'] == 'test_title'
        assert request.status_code == 201

    def test_note_post_400(self, client):
        request = client.post(f'{self.url}', **self.headers, data={
            'title': 'test_title',
            'user': self.user.id,
        })
        response = request.json()
        assert response['description'] == ['This field is required.']
        assert request.status_code == 400

    def test_note_post_401(self, client):
        request = client.post(f'{self.url}', data={
            'title': 'test_title',
            'description': 'test_description',
            'user': self.user.id,
        })
        response = request.json()
        assert response['detail'] == 'Authentication credentials were not provided.'
        assert request.status_code == 401

    def test_note_destroy(self, client):
        request = client.delete(f'{self.url}{self.note.id}/', **self.headers)
        assert request.status_code == 204

    def test_note_destroy_401(self, client):
        request = client.delete(f'{self.url}{self.note.id}/')
        response = request.json()
        assert response['detail'] == 'Authentication credentials were not provided.'
        assert request.status_code == 401

    def test_note_destroy_403(self, client):
        request = client.delete(f'{self.url}{self.note2.id}/', **self.headers)
        response = request.json()
        assert response['detail'] == 'You do not have permission to perform this action.'
        assert request.status_code == 403

    def test_note_destroy_404(self, client):
        request = client.delete(f'{self.url}999/', **self.headers)
        response = request.json()
        assert response['detail'] == 'No Note matches the given query.'
        assert request.status_code == 404

