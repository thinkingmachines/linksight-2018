from django.conf import settings
from django.db import models


class Survey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=100)
    profession = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    has_gis_experience = models.BooleanField(
        verbose_name='Do you have GIS experience?')
    source = models.TextField(verbose_name='How did you hear about LinkSight?')
    usecase = models.TextField(verbose_name='How can LinkSight help you?')

    def __str__(self):
        return self.user.get_full_name()
