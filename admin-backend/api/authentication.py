# api/authentication.py
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import UserToken
from django.utils import timezone


def verify_token(token):
    """Vérifie un token et retourne l'utilisateur associé."""
    try:
        ut = UserToken.objects.get(
            token=token, is_active=True, expires_at__gt=timezone.now()
        )
        return ut.user
    except UserToken.DoesNotExist:
        return None


class BearerTokenAuthentication(BaseAuthentication):
    """Authentifie l'utilisateur via un Bearer token maison."""

    def authenticate(self, request):
        header = request.headers.get('Authorization')
        if not header or not header.startswith('Bearer '):
            return None
        token = header.split(' ', 1)[1].strip()
        if not token:
            return None
        user = verify_token(token)
        if not user:
            raise AuthenticationFailed('Token invalide ou expiré')
        return (user, token)