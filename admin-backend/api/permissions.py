# api/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperIT(BasePermission):
    """
    Autorise uniquement les utilisateurs avec role='it_admin'.
    Le SuperIT a tous les droits sur la plateforme.
    """
    message = "Accès réservé au SuperIT."

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, 'role', None) == 'it_admin'
        )


class IsAdminOrSuperIT(BasePermission):
    """
    Autorise les administrateurs (role='admin') et le SuperIT (role='it_admin').
    Utilisé pour les CRUD de contenu : plantes, projets, activités, publications.
    """
    message = "Accès réservé aux administrateurs."

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, 'role', None) in ('admin', 'it_admin')
        )


class ReadOnlyOrAdminOrSuperIT(BasePermission):
    """
    Lecture publique (GET/HEAD/OPTIONS), écriture réservée aux admins/SuperIT.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, 'role', None) in ('admin', 'it_admin')
        )