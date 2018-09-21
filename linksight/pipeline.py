from django.shortcuts import redirect
from linksight.settings import HOST


def auth_allowed(backend, details, response, *args, **kwargs):
    if not backend.auth_allowed(response, details):
        return redirect('{}/?login-error'.format(HOST))
