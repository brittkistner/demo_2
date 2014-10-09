from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    fb_auth_key = models.CharField() #length?

    def __unicode__(self):
        return u"{}".format(self.first_name)

class Receiver(models.Model):
    user = models.ForeignKey(User, related_name="receivers")
    name = models.CharField(max_length=30)
    birthday = models.DateField() #what will this look like?
    age = models.IntegerField(default=None)

    def __unicode__(self):
        return u"{}".format(self.name)

class Words(models.Model):
    receiver = models.ForeignKey(Receiver, related_name="words")
    name = models.CharField(max_length=30)
    ranking = models.IntegerField(default=None)

    #think about adding models to increment/decrement rankings.
    #May need a model to sum up ranking for each user and another method for applying a weighting
