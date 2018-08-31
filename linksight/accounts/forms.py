from django import forms
from django.utils.translation import ugettext_lazy as _
from registration.forms import RegistrationForm


class RegistrationWithSurveyForm(RegistrationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    contact_number = forms.CharField(required=False)
    profession = forms.CharField(required=False)
    organization = forms.CharField(required=False)
    has_gis_experience = forms.NullBooleanField(
        widget=forms.RadioSelect(choices=[
            (True, 'Yes'),
            (False, 'No'),
        ]),
        label=_('Do you have GIS experience?'),
        required=True,
        initial=False)
    source = forms.CharField(
        widget=forms.Textarea,
        label=_('How did you hear about LinkSight?'))
    usecase = forms.CharField(
        widget=forms.Textarea,
        label=_('How can LinkSight help you?'))

