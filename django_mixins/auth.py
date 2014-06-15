

from django.dispatch import receiver
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.signals import user_logged_in, user_logged_out


CurrentUser = AnonymousUser() 


@receiver(user_logged_in)
def userLoggedInReceiver(sender, **kwargs):

    CurrentUser = kwargs['user']


@receiver(user_logged_in)
def userLoggedInReceiver(sender, **kwargs):

    CurrentUser = AnonymousUser()

