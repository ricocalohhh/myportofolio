import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from main.models import Experience


class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username='owner_ex', email='owner@example.com', password='safe-pass-123'
        )
        self.user = User.objects.create_user(username='user_ex', password='safe-pass-123')
        self.editor = User.objects.create_user(username='editor_ex', password='safe-pass-123')
        self.editor.groups.add(Group.objects.create(name='Editor'))
        self.exp = Experience.objects.create(
            title='Pengalaman Awal', description='Belajar Django', category='internship',
            started_at='2024-01-01T00:00:00Z',
        )
        self.list_url = reverse('api:experience-list')
        self.detail_url = reverse('api:experience-detail', args=[self.exp.pk])
        self.star_url = reverse('api:experience-star', args=[self.exp.pk])
        self.payload = {
            'title': 'Pengalaman Baru', 'description': 'Membuat aplikasi',
            'category': 'internship', 'started_at': '2024-01-01T00:00:00Z',
        }

    def test_public_read_search_and_missing(self):
        result = self.client.get(self.list_url, {'title': 'AWAL'})
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.data), 1)
        self.assertFalse(result.data[0]['is_starred'])
        self.assertNotIn('email', result.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, 200)
        missing = reverse('api:experience-detail', args=[uuid.uuid4()])
        self.assertEqual(self.client.get(missing).status_code, 404)

    def test_guest_and_user_cannot_write(self):
        for actor in (None, self.user):
            self.client.force_authenticate(user=actor)
            self.assertEqual(self.client.post(self.list_url, self.payload, format='json').status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {'title': 'Diubah'}, format='json').status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
            self.assertEqual(Experience.objects.count(), 1)
            self.exp.refresh_from_db()
            self.assertEqual(self.exp.title, 'Pengalaman Awal')

    def test_editor_can_patch_but_not_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {'title': 'Diedit'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.exp.refresh_from_db()
        self.assertEqual(self.exp.title, 'Diedit')
        self.assertEqual(self.client.post(self.list_url, self.payload, format='json').status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)
        self.assertTrue(Experience.objects.filter(pk=self.exp.pk, title='Diedit').exists())

    def test_owner_creates_and_deletes(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Experience.objects.filter(pk=response.data['id']).exists())
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Experience.objects.filter(pk=self.exp.pk).exists())

    def test_validation_and_cleaning(self):
        self.client.force_authenticate(user=self.owner)
        invalid = {**self.payload, 'title': '<b></b>'}
        result = self.client.post(self.list_url, invalid, format='json')
        self.assertEqual(result.status_code, 400)
        self.assertIn('title', result.data)
        self.assertEqual(Experience.objects.count(), 1)
        result = self.client.post(self.list_url, {
            **self.payload, 'description': '<b>Aman</b>',
        }, format='json')
        self.assertEqual(result.status_code, 201)
        self.assertEqual(Experience.objects.get(pk=result.data['id']).description, 'Aman')
        result = self.client.patch(self.detail_url, {
            'ended_at': '2023-01-01T00:00:00Z',
        }, format='json')
        self.assertEqual(result.status_code, 400)
        self.exp.refresh_from_db()
        self.assertIsNone(self.exp.ended_at)

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, 403)
        self.assertEqual(self.exp.starred_by.count(), 0)
        self.client.force_authenticate(user=self.user)
        result = self.client.post(self.star_url)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(result.data['is_starred'])
        self.assertEqual(result.data['star_count'], 1)
        self.assertTrue(self.exp.starred_by.filter(pk=self.user.pk).exists())
        result = self.client.post(self.star_url)
        self.assertFalse(result.data['is_starred'])
        self.assertEqual(self.exp.starred_by.count(), 0)

    def test_session_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username='owner_ex', password='safe-pass-123'))
        result = client.post(self.list_url, self.payload, format='json')
        self.assertEqual(result.status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)