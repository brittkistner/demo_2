from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # fb_auth_key = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return u"{}".format(self.first_name)

class Receiver(models.Model):
    user = models.ForeignKey(User, related_name="receivers")
    name = models.TextField()
    birthday = models.DateField() #what will this look like?
    age = models.IntegerField(default=None)
    img = models.ImageField(upload_to='receiver_images', blank=True, null=True)

    def __unicode__(self):
        return u"{}".format(self.name)

class WordReceiver(models.Model):
    receiver = models.ForeignKey(Receiver, related_name="words")
    name = models.CharField(max_length=255)
    ranking = models.IntegerField(default=0)

    #think about adding models to increment/decrement rankings.
    #May need a model to sum up ranking for each user and another method for applying a weighting
    #another to find top words

class Product(models.Model):
    receivers = models.ManyToManyField(Receiver, through="ProductReceiver", related_name="products",default=None)
    asin = models.CharField(max_length=30, primary_key=True)
    price = models.FloatField(null=True)
    image_url = models.TextField(null=True)
    name = models.TextField(null=True)
    review = models.TextField(default=None)
    link = models.TextField(null=True)

    def __unicode__(self):
        return u"{}".format(self.name)

    def words(self):
        word_dict = {}
        if self.features:
            features_list = self.features.all()
            for feature in features_list:
                word_list = feature.feature.split(' ')
                for word in word_list:
                    if word in word_dict:
                        word_dict[word] += 1
                    else:
                        word_dict[word] = 1
        elif self.review:
            word_list = self.review.split(' ')
            for word in word_list:
                if word in word_dict:
                    word_dict[word] += 1
                else:
                    word_dict[word] = 1
        else:
            title_list = self.name.split(' ')
            for word in title_list:
                if word in word_dict:
                    word_dict[word] += 1
                else:
                    word_dict[word] = 1
        return word_dict

class Feature(models.Model):
    product = models.ForeignKey(Product, related_name="features")
    feature = models.TextField(default=None)

    def __unicode__(self):
        return u"{}".format(self.feature)

# class Review(models.Model):
#     product = models.ForeignKey(Product, related_name="features")
#     review = models.TextField(default=None)

class ProductReceiver(models.Model):
    score = models.IntegerField(default=0)
    product = models.ForeignKey(Product, related_name="product")
    receiver = models.ForeignKey(Receiver,related_name="receiver")