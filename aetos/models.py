# Package Imports
from model_utils.models import TimeStampedModel

# Django Imports
from django.db import models


class AetosModel(TimeStampedModel):
    is_active = models.BooleanField(default=False)
    meta = models.TextField(default='{}')

    class Meta:
        abstract = True
