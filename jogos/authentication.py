from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed


class FlexibleTokenAuthentication(TokenAuthentication):
    """
    Aceita ambos os formatos:
    - Authorization: Token <key>
    - Authorization: Bearer <key>
    """
    
    keyword = 'Token'

    def get_model(self):
        if self.model is not None:
            return self.model
        from rest_framework.authtoken.models import Token
        return Token

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth:
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise AuthenticationFailed(msg)

        if len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise AuthenticationFailed(msg)

        try:
            auth_type = auth[0].decode()
            auth_string = auth[1].decode()
        except UnicodeDecodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise AuthenticationFailed(msg)

        # Aceitar tanto "Token" quanto "Bearer"
        if auth_type.lower() not in ('token', 'bearer'):
            msg = f'Invalid token header. Token type must be Token or Bearer. Got: {auth_type}'
            raise AuthenticationFailed(msg)

        return self.authenticate_credentials(auth_string)

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted.')

        return (token.user, token)
