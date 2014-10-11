from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # fb_auth_key = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return u"{}".format(self.first_name)

class Receiver(models.Model):
    user = models.ForeignKey(User, related_name="receivers")
    name = models.CharField(max_length=30)
    birthday = models.DateField() #what will this look like?
    age = models.IntegerField(default=None)

    def __unicode__(self):
        return u"{}".format(self.name)

class WordReceiver(models.Model):
    receiver = models.ForeignKey(Receiver, related_name="words")
    name = models.CharField(max_length=30)
    ranking = models.IntegerField(default=0)

    #think about adding models to increment/decrement rankings.
    #May need a model to sum up ranking for each user and another method for applying a weighting
    #another to find top words

class Product(models.Model):
    receivers = models.ManyToManyField(Receiver, through="ProductReceiver", related_name="products",default=None)
    asin = models.CharField(max_length=30, primary_key=True)
    price = models.FloatField()
    image_url = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    # round = models.IntegerField(default=None)
    #anything else?

class ProductReceiver(models.Model):
    score = models.IntegerField(default=0)
    product = models.ForeignKey(Product, related_name="product")
    receiver = models.ForeignKey(Receiver,related_name="receiver")