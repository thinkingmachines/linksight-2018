import csv
import json
from django.conf import settings

from social_core.exceptions import AuthAlreadyAssociated, AuthException, AuthForbidden


def auth_allowed(backend, details, response, *args, **kwargs):
    file = settings.APPROVED_EMAILS

    json_data = [json.dumps(d) for d in csv.DictReader(open(file))]
    approved_emails = [json.loads(row)['E-mail'] for row in json_data]

    email = details.get('email')

    if email not in approved_emails:
        raise AuthForbidden(backend)
