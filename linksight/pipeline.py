from apiclient.discovery import build
from django.shortcuts import redirect
from linksight.settings import (APPROVED_EMAILS_ROW_KEY,
                                APPROVED_EMAILS_SHEET_ID,
                                APPROVED_EMAILS_SHEET_RANGE, HOST)


def get_sheet_values(spreadsheet_id, sheet_range):
    service = build('sheets', 'v4')
    client = service.spreadsheets()
    values = client.values().get(
        spreadsheetId=spreadsheet_id,
        range=sheet_range).execute().get('values', [])
    fields = values.pop(0)
    for value in values:
        yield dict(zip(fields, value))


def auth_allowed(backend, details, response, *args, **kwargs):
    approved_emails = [
        row.get(APPROVED_EMAILS_ROW_KEY)
        for row in get_sheet_values(
            APPROVED_EMAILS_SHEET_ID,
            APPROVED_EMAILS_SHEET_RANGE)
    ]
    email = details.get('email')
    if email not in approved_emails:
        return redirect('{}/?unapproved={}'.format(HOST, email))
