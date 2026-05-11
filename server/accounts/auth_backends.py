# accounts/auth_backends.py
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

class CustomOIDCBackend(OIDCAuthenticationBackend):
    def update_user(self, user, claims):
        realm_access = claims.get('realm_access', {})
        roles = realm_access.get('roles', [])

        if 'django_root' in roles:
            user.is_superuser = True
            user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff = False
            
        user.save()
        return user

    def create_user(self, claims):
        user = super(CustomOIDCBackend, self).create_user(claims)
        return self.update_user(user, claims)