import json
from django.shortcuts import redirect
from linksight.settings import HOST, APPROVED_EMAILS_SHEETS_ID

from apiclient.discovery import build


def get_sheets_service():
    return build('sheets', 'v4')


def get_sheets_client():
    service = get_sheets_service()
    return service.spreadsheets()


def get_sheet_values(spreadsheet_id, sheet_range):
    client = get_sheets_client()
    values = client.values().get(
        spreadsheetId=spreadsheet_id,
        range=sheet_range).execute().get('values', [])
    fields = values.pop(0)
    for value in values:
        yield dict(zip(fields, value))


def auth_allowed(backend, details, response, *args, **kwargs):
    approved_emails = [json.dumps(row) for row in get_sheet_values(APPROVED_EMAILS_SHEETS_ID,
                                                                   'Sheet1!A')]

    email = details.get('email')

    if email not in approved_emails:
        return redirect('{}/?login-error'.format(HOST))
