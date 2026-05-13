from rest_framework.authentication import TokenAuthentication, get_authorization_header


class FlexibleTokenAuthentication(TokenAuthentication):
    """Accept both Authorization: Token <key> and Bearer <key>."""

    def authenticate(self, request):
        auth_header = get_authorization_header(request).split()
        if auth_header and auth_header[0].lower() == b'bearer':
            auth_header[0] = b'token'
            request.META['HTTP_AUTHORIZATION'] = b' '.join(auth_header).decode('utf-8')
        return super().authenticate(request)
