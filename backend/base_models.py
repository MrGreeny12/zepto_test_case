from django.contrib.auth import get_user_model
from django.db import models


class BaseModel(models.Model):
    owner = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Создал'
    )

    default_manager = models.Manager()

    class Meta:
        abstract = True
