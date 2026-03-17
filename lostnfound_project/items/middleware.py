from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    OPEN_URLS = [
        '/',
        '/accounts/login/',
        '/accounts/register/',
        '/accounts/password-reset/',
        '/accounts/password-reset-done/',
        '/admin/',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        # Allow open URLs, admin, static, media, search API
        is_open = (
            path in self.OPEN_URLS or
            path.startswith('/admin/') or
            path.startswith('/static/') or
            path.startswith('/media/') or
            path.startswith('/accounts/password-reset') or
            path == '/items/search/'
        )

        if not is_open and not request.user.is_authenticated:
            # Store where they were going
            return redirect(f'/accounts/login/?next={path}')

        return self.get_response(request)
