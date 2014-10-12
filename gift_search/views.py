import json
from django.contrib.auth import authenticate, login
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
# import facebook
from amazon.api import AmazonAPI
# from social.backends.google import GooglePlusAuth
from django.views.decorators.csrf import csrf_exempt
from demo2.settings import AMAZON_ASSOC_TAG, config, AMAZON_SECRET_KEY, \
    AMAZON_ACCESS_KEY  # SOCIAL_AUTH_GOOGLE_PLUS_KEY,
import amazonproduct
from gift_search.forms import EmailUserCreationForm
from gift_search.models import Product, WordReceiver, Receiver, ProductReceiver, Feature
import random

# plus_scope = ' '.join(GooglePlusAuth.DEFAULT_SCOPE)
amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)
receiver = None
import time

# ##############
# REGISTRATION #
###############


def register(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # text_content = 'Thank you for signing up for our website, {}'.format(user.username)
            # html_content = '<h2>Thanks {} {} for signing up!</h2> <div>You joined at {}.  I hope you enjoy using our site</div>'.format(user.first_name, user.last_name, user.date_joined)
            # msg = EmailMultiAlternatives("Welcome!", text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            login(request, new_user)
            return redirect("receivers")

    else:
        form = EmailUserCreationForm()

    return render(request, "registration/register.html", {
        'form': form,
    })


def add_friend(request):
    pass


############################
# DISPLAY USER'S RECEIVERS #
############################

def receivers(request):
    user = request.user
    receivers = user.receivers.all()
    print receivers
    data = {
        'receivers': receivers
    }
    return render(request, "receivers.html", data)


#####################################
# DISPLAY RECEIVER PROFILE FOR USER #
#####################################

def receiver_page(request, receiver_id):
    product_list = Product.objects.all()
    receiver = Receiver.objects.get(pk=receiver_id)
    length = len(product_list)
    product_to_rank = product_list[random.randrange(length)]
    products = receiver.products.all()
    data = {
        'product_to_rank': product_to_rank,
        'products': products
    }
    return render(request, "receivers_page.html", data)


#####################
# RANKING A PRODUCT #
####################
def create_words(receiver, asin, score):
    print "in word creation"
    if score == "up":
        score = 1
    else:
        score = -1

    product = Product.objects.get(asin=asin)
    print product.review

    if product.features.all():
        features_list = product.features.all()
        for feature in features_list:
            word_list = feature.feature.split(' ')
            for word in word_list:
                try:
                    receiver_word = WordReceiver.objects.get(name=word, receiver=receiver)
                    receiver_word.ranking += score
                    receiver_word.save()
                except:
                    WordReceiver(receiver=receiver, name=word, ranking=score).save()
    #if not, check if review exists for product
    elif product.review != "N/A":
        review = product.review
        word_list = review.split(' ')
        for word in word_list:
            print word
            try:
                receiver_word = WordReceiver.objects.get(name=word, receiver=receiver)
                receiver_word.ranking += score
                receiver_word.save()
            except:
                WordReceiver(receiver=receiver, name=word, ranking=score).save()
    #if not then use name
    else:
        name = product.name
        word_list = name.split(' ')
        for word in word_list:
            try:
                receiver_word = WordReceiver.objects.get(name=word, receiver=receiver)
                receiver_word.ranking += score
                receiver_word.save()
            except:
                WordReceiver(receiver=receiver, name=word, ranking=score).save()

    return True

#Query on words for top three
def get_top_three(receiver):
    print "in top three"
    word_list = receiver.words.filter(name__iregex=r'^.{7,}$').order_by('ranking')[:3]
    print word_list
    return word_list


def create_product(receiver, amazon_product):
    print amazon_product
    price = amazon_product.price_and_currency[0]  #(30.0,'USD')
    image_url = amazon_product.large_image_url
    name = amazon_product.title
    asin = amazon_product.asin
    product = Product(asin=asin, price=price, image_url=image_url, name=name, review="N/A")
    product.save()
    if amazon_product.features:
        features_list = amazon_product.features
        for feature in features_list:
            Feature(product=product, feature=feature).save()
    elif amazon_product.editorial_review:
        review = amazon_product.editorial_review
        product.review = review
        product.save()
    time.sleep(1)

    return True


def get_products_from_Amazon_update_create_product(word_list):
    #MAKE COMMENT
    print "in get_new_products"
    products = Product.objects.all()
    for word in word_list:
        print word.name
        new_products = amazon.search(Keywords=word.name, SearchIndex='All')
        for i, product in enumerate(new_products):
            try:
                product = Product.objects.get(asin=product.asin)
            except:
                create_product(receiver, product)
        return True


@csrf_exempt
def create_productreceiver(request, receiver_id, score, asin):
    #MAKE COMMENT
    print 'made it to productreceiver'
    print receiver_id
    receiver = Receiver.objects.get(pk=int(receiver_id))
    try:
        product_receiver = ProductReceiver.objects.get(product__asin=asin, receiver=receiver)
        print "break1"
    except:
        product_receiver = ProductReceiver(product=Product.objects.get(asin=asin), receiver=receiver).save()
        print "break2"

    #a  product has been added to the receiver list, must create and rank the words
    create_words(receiver, asin, score)

    #Returns Top 3 Ranking words
    word_list = get_top_three(receiver)
    print word_list

    #Search Amazon for products given word_list
    get_products_from_Amazon_update_create_product(word_list)

    # response = serializers.serialize('json', [True])
    return HttpResponse('true', content_type='application/json')


##################
# UPDATE HISTORY #
##################
@csrf_exempt
def update_history(request, receiver_id):
    receiver = Receiver.objects.get(pk=int(receiver_id))
    products = receiver.products.all()
    data = {
        'products': products,
    }

    return render(request, "update_history.html", data)



##########################
# UPDATE RECOMMENDATIONS #
#########################
# @csrf_exempt
def get_top_recommendations(request, receiver_id):
    receiver = Receiver.objects.get(pk=int(receiver_id))
    products = Product.objects.all()
    products_list = []
    for product in products:
        score = 0
        product_words = product.words()
        for receiver_word in receiver.words.all():
            if receiver_word.name in product_words:
                score += receiver_word.ranking * product_words[receiver_word.name]
        products_list.append((product, score))
    products_list = sorted(products_list, key=lambda x: x[1])
    products_list = filter(lambda x: x[0] not in receiver.products.all(), products_list)
    top_products = products_list[:3]
    for product_tuple in top_products:
        print product_tuple[0]

    data = {
        'top_products' : top_products
    }
    return render(request, "top_products.html", data)

    ####################
    # LOAD NEW PRODUCT #
    ####################
















    # def get_gifts(request, receiver_id=2):
    #     receiver = Receiver.objects.get(pk=receiver_id)
    #
    #
    #     #ITEM LOOKUP-Python Amazon Simple Product API#
    #     item_ids = {'Books':'1423146735',
    #                 'Music':'B00MRHANNI',
    #                 'Mens':'B00INNBILG',
    #                 'Womens': 'B00KGT9GUU',
    #                 'Electronics': 'B00DR0PDNE',
    #                 'Gourmet Food': 'B008UOUGN4',
    #                 'Movies & TV': 'B00NTSYP3S',
    #                 "Women's Jewelry": 'B00BC4IR0I',
    #                 'Sports & Outdoors':'B004J2GUOU',
    #                 'Toys & Games': 'B004S8F7QM',
    #                 'Video Games': 'B00DD0B1R0',
    #                 }
    #
    #     #Creates Product and Word instances for each item. Iterates through item_ids, creating products.
    #     # After product created, sent to create_words function to create a word instance for the features list.
    #     # This features list will then be incremented or decremented based on user feedback.
    #     products_dict = {}
    #     for item in item_ids:
    #         receiver = Receiver.objects.get(pk=receiver_id)
    #         amazon_product = amazon.lookup(ItemId=item_ids[item])
    #         price = amazon_product.price_and_currency[0] #(30.0,'USD')
    #         image_url = amazon_product.large_image_url
    #         name = amazon_product.title
    #         asin = amazon_product.asin
    #         product = Product(asin=asin, price=price, image_url=image_url, name=name, review="N/A").save()
    #         if amazon_product.features != []:
    #             features_list = amazon_product.features
    #             for feature in features_list:
    #                 Feature(product=product, feature=feature).save()
    #         elif amazon_product.editorial_review !=[]:
    #             review = amazon_product.editorial_review
    #             product.review = review
    #             product.save()
    #         products_dict[asin]= product
    #         ProductReceiver(product=product,receiver=receiver).save()
    #         time.sleep(1)
    #
    #     data = {
    #        'products': products_dict
    #     }
    #
    #     print data
    #     return render(request, "get_gifts.html", data)










    #GIFT CARD??
    # 'Gift Card': 'B00A48G0D4',



    # user_social_auth = request.user.social_auth.filter(provider='facebook').first()
    # graph = facebook.GraphAPI(user_social_auth.extra_data['access_token'])
    # profile_data = graph.get_object("me")
    # user_id = graph.get_object("me")["id"]
    # print user_id
    # friends = graph.get_object("me/taggable_friends") #array
    # print friends
    # # profile_data = json.dumps(profile_data['results'])
    # # user = graph.get_object(profile_data["name"])
    # # print user
    #create a receiver object and set in the window?


# def home(request):
#     # data = {
#     #     "plus_scope": plus_scope,
#     #     'plus_id':  SOCIAL_AUTH_GOOGLE_PLUS_KEY
#     # }
#     #LOGIN PAGE
#     return render(request, "home.html")
