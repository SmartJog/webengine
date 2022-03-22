from django.db import models
from django.contrib.auth.models import User


class UserSetting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=128)
    value = models.CharField(max_length=512)

    def __unicode__(self):
        return self.key + ": " + self.value
