from django.contrib.postgres.functions import RandomUUID
from django.db import models


class Dataset(models.Model):
    id = models.UUIDField(primary_key=True, default=RandomUUID(),
                          editable=False)
    file = models.FileField(upload_to='datasets/')
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name or self.file.name
