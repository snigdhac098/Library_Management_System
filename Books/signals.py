from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from Books.models import UserAccount

@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        UserAccount.objects.create(user=instance)
