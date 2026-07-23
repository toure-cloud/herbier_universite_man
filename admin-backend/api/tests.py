from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed

from .models import SuperAdmin, UserToken
from .serializers import PlanteSerializer
from .views import BearerTokenAuthentication


class BearerTokenAuthenticationTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = SuperAdmin.objects.create(
            email='test@example.com',
            nom='Test User',
            telephone='0102030405',
            password='dummy',
            is_active=True,
        )
        self.token = 'test-token-123'
        self.user_token = UserToken.objects.create(
            user=self.user,
            token=self.token,
            expires_at=timezone.now() + timezone.timedelta(days=1),
            is_active=True,
        )

    def test_authenticates_user_with_valid_bearer_token(self):
        request = self.factory.get('/api/plantes/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        auth = BearerTokenAuthentication()

        user, token = auth.authenticate(request)

        self.assertEqual(user, self.user)
        self.assertEqual(token, self.token)

    def test_rejects_invalid_bearer_token(self):
        request = self.factory.get('/api/plantes/', HTTP_AUTHORIZATION='Bearer invalid-token')
        auth = BearerTokenAuthentication()

        with self.assertRaises(AuthenticationFailed):
            auth.authenticate(request)

    def test_accepts_long_image_payload_for_plants(self):
        long_image = 'data:image/png;base64,' + 'a' * 600
        serializer = PlanteSerializer(data={
            'nom': 'Test plante',
            'famille': 'Fabaceae',
            'nom_scientifique': 'Test scientific',
            'description': 'Description',
            'habitat': 'Habitat',
            'statut_conservation': 'En danger',
            'actif': True,
            'image': long_image,
        })

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_accepts_uploaded_image_file_for_plants(self):
        uploaded_file = SimpleUploadedFile(
            'plante.png',
            b'fake-image-data',
            content_type='image/png',
        )
        request = self.factory.post('/api/plantes/')
        serializer = PlanteSerializer(data={
            'nom': 'Test plante upload',
            'famille': 'Fabaceae',
            'description': 'Description',
            'habitat': 'Habitat',
            'statut_conservation': 'En danger',
            'actif': True,
            'image': uploaded_file,
        }, context={'request': request})

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertTrue(serializer.validated_data['image'].startswith('http://'))
