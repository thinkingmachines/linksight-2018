import uuid

import pandas as pd

from django.db import models


class Dataset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    file = models.FileField(upload_to='datasets/')
    name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or self.file.name

    def preview(self):
        with self.file.open() as f:
            df = pd.read_csv(f)
            return df.head().to_dict()
