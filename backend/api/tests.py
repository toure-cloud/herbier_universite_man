from unittest.mock import Mock, patch

from django.test import SimpleTestCase
from django.test.client import RequestFactory

from .views import proxy_to_admin_backend


class ProxyToAdminBackendTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('api.views.requests.get')
    def test_proxy_to_admin_backend_returns_admin_payload(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1, "nom": "Test plante"}]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        request = self.factory.get('/api/plantes/')
        response = proxy_to_admin_backend(request, 'plantes')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{"id": 1, "nom": "Test plante"}])
