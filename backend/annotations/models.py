from django.db import models
from django.contrib.auth.models import User


class HypothesisAuthentication(models.Model):
    '''Model with a one-to-one connection to the user to save the
    authentication to the Hypothesis server'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_token = models.CharField(max_length=256, blank=True, default='')
    hypothesis_username = models.CharField(max_length=256, blank=True,
                                           default='')

    def __str__(self):
        return str(self.user)
