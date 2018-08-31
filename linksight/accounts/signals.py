def record_survey(sender, user, request, **kwargs):
    from linksight.accounts.forms import RegistrationWithSurveyForm
    from linksight.accounts.models import Survey
    from registration.forms import RegistrationForm

    form = RegistrationWithSurveyForm(request.POST)
    form.is_valid()

    survey_data = {
        field: value
        for field, value in form.cleaned_data.items()
        # Exclude user fields
        if field not in RegistrationForm.base_fields.keys()
    }

    user.first_name = survey_data.pop('first_name')
    user.last_name = survey_data.pop('last_name')
    user.save()

    Survey.objects.create(
        user=user,
        **survey_data
    )
