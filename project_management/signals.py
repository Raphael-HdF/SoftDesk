from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Contributor


@receiver(pre_save, sender=Contributor)
def my_handler(sender, **kwargs):
    pass
