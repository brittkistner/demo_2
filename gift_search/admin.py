from django.contrib import admin
from gift_search.models import Receiver, Product, WordReceiver, User, ProductReceiver, Feature

admin.site.register(Receiver)
admin.site.register(Product)

admin.site.register(WordReceiver)
admin.site.register(User)
admin.site.register(ProductReceiver)
admin.site.register(Feature)