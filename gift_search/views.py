import datetime
import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
# import facebook
from amazon.api import AmazonAPI
# from social.backends.google import GooglePlusAuth
from django.views.decorators.csrf import csrf_exempt
from demo2.settings import AMAZON_ASSOC_TAG, config, AMAZON_SECRET_KEY, \
    AMAZON_ACCESS_KEY, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_ASSOCIATE_TAG  # SOCIAL_AUTH_GOOGLE_PLUS_KEY,
import amazonproduct
from gift_search.forms import EmailUserCreationForm, CreateReceiver
from gift_search.models import Product, WordReceiver, Receiver, ProductReceiver, Feature
import random
import bottlenose
from xml.dom import minidom


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


# def add_receiver(request):
#     data = {"create_receiver": CreateReceiver()}
#     if request.method == "POST":
#         form = CreateReceiver(request.POST, request.FILES)
#         if form.is_valid():
#             receiver = Receiver(user=request.user,
#                      name=form.cleaned_data['name'],
#                      birthday=form.cleaned_data['birthday'],
#                      age=form.cleaned_data['age'],
#                      img=form.cleaned_data)
#             response = serializers.serialize('json', [receiver])
#             return HttpResponse(response, content_type='application/json')
#         else:
#             data = {"create_receiver": CreateReceiver()}
#             return render(request, "add_receiver_form.html",data)
#
#     return render(request, "add_receiver_form.html")

############################
# DISPLAY USER'S RECEIVERS #
############################
@login_required()
def receivers(request):
    today = datetime.date.today()
    end_date = today + datetime.timedelta(days=31)
    user = request.user
    receiver_list = user.receivers.all()
    birthday_receivers = []
    for receiver in receiver_list:
        # This logic could be moved to the Receiver model
        # Should also put in some comments to explain what you're checking for and why you need to replace the year to today's year
        birthday_no_year = receiver.birthday
        birthday_no_year=birthday_no_year.replace(year=today.year)
        print birthday_no_year
        if birthday_no_year >= today and birthday_no_year <= end_date:
            birthday_receivers.append(receiver)
    data = {
        'receivers': birthday_receivers
    }
    return render(request, "receivers.html", data)

####################
# Get Product URL #
####################

# def getText(nodelist):
#     rc = []
#     for node in nodelist:
#         if node.nodeType == node.TEXT_NODE:
#             rc.append(node.data)
#     return ''.join(rc)
#
# def get_url(item_id):
#     amazon = bottlenose.Amazon(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_ASSOCIATE_TAG)
#     item = amazon.ItemLookup(ItemId=item_id)
#     tree = minidom.parseString(item)
#     detail = tree.getElementsByTagName("DetailPageURL")[0]
#     link = "{}".format(getText(detail.childNodes))
#     time.sleep(1)
#     return link

####################
# LOAD NEW PRODUCT #
####################


def init_products(receiver):

    #ITEM LOOKUP-Python Amazon Simple Product API#
    item_ids = {
        'Books':'1423146735',
        'Music':'B00MRHANNI',
        'Mens':'B00INNBILG',
        'Womens': 'B00KGT9GUU',
        'Electronics': 'B00DR0PDNE',
        'Gourmet Food': 'B008UOUGN4',
        'Movies & TV': 'B00NTSYP3S',
        "Women's Jewelry": 'B00BC4IR0I',
        'Sports & Outdoors':'B004J2GUOU',
        'Toys & Games': 'B004S8F7QM',
        'Video Games': 'B00DD0B1R0',
        'Gift Card': 'B00A48G0D4',
    }

    #Creates Product instance for each item. Iterates through item_ids, creating products.
    # After product created, sent to create_words function to create a word instance for the features list.
    # This features list will then be incremented or decremented based on user feedback.

    for item in item_ids:
        # Might be good to put some of this logic in a specific function, maybe on the Product model since
        # you're basically trying to save a valid amazon product to a local Product
        amazon_product = amazon.lookup(ItemId=item_ids[item])
        # product.get_attribute('ProductGroup')
        
        # It's best practice to "except" a specific error, not just any
        # Do you really want to return False in all of these cases or should you just continue to the next item ID?
        try:
            price = amazon_product.price_and_currency[0]  #(30.0,'USD')
        except:
            return False
        try:
            image_url = amazon_product.large_image_url
        except:
            return False
        name = amazon_product.title
        if name == None:
            return False
        asin = amazon_product.asin
        try:
            link = amazon_product._safe_get_element_text('DetailPageURL')
        except:
            return False
        product = Product(asin=asin, price=price, image_url=image_url, name=name, review="N/A", link=link)
        product.save()
        if amazon_product.features:
            features_list = amazon_product.features
            for feature in features_list:
                Feature(product=product, feature=feature).save()
        elif amazon_product.editorial_review:
            review = amazon_product.editorial_review
            product.review = review
            product.save()
        time.sleep(.25)

    return True



#########################
# Initial Receiver Page #
#########################
def init_receiver_page(receiver):
    data = {}
    # Could just get a random product from the database - Product.objects.order_by('?')[:1]
    all_products = Product.objects.all()
    length = len(all_products)
    product_to_rank = all_products[random.randrange(length)]
    data['product_to_rank'] = product_to_rank
    # Product History #
    product_history = receiver.products.all()
    data['product_history'] = product_history
    # Top Products #
    products_list = []
    for product in all_products:
        score = 0
        product_words = product.words()
        # could do some of the filtering in the query instead of python? receiver.words.filter(name__in=product_words)
        for receiver_word in receiver.words.all():
            if receiver_word.name in product_words:
                score += receiver_word.ranking * product_words[receiver_word.name]
        products_list.append((product, score))
    products_list = sorted(products_list, key=lambda x: x[1])
    products_list = filter(lambda x: x[0] not in receiver.products.all(), products_list)
    top_products = products_list[:3]
    print top_products[0][0]
    data['top_products'] = top_products


    return data


#####################################
# DISPLAY RECEIVER PROFILE FOR USER #
#####################################

@login_required()
def receiver_page(request, receiver_id):
    receiver = Receiver.objects.get(pk=receiver_id)
    # Could use Product.objects.exists() or Product.objects.count() > 0 instead
    if Product.objects.all():
        data = init_receiver_page(receiver)
    else:
        init_products(receiver)
        data = init_receiver_page(receiver)
    gift_card = Product.objects.get(asin='B00A48G0D4')
    data["gift_card"] = gift_card
    data["receiver"] = receiver
    return render(request, "receivers_page.html", data)

#####################
# RANKING A PRODUCT #
####################
def create_words(receiver, asin, score):
    if score == "up":
        score = 1
    else:
        score = -1

    product = Product.objects.get(asin=asin)
    print product.review

    # These if statements all seem fairly similar, could abstract out the looping `for word in word_list` part 
    # and WordReceiver creation into a separate function you call
    if product.features.all():
        features_list = product.features.all()
        for feature in features_list:
            word_list = feature.feature.split(' ')
            for word in word_list:
                try:
                    receiver_word = WordReceiver.objects.get(name=word, receiver=receiver)
                    receiver_word.ranking += score
                    receiver_word.save()
                except WordReceiver.DoesNotExist:
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
            except WordReceiver.DoesNotExist:
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
            except WordReceiver.DoesNotExist:
                WordReceiver(receiver=receiver, name=word, ranking=score).save()

    return True


#Query on words for top three
def get_top_three(receiver):
    word_list = receiver.words.filter(name__iregex=r'^.{5,}$').order_by('ranking')[:3]
    return word_list


def create_product(receiver, amazon_product):
    # This looks really similar to init_products(), could make this DRYer
    try:
        price = amazon_product.price_and_currency[0]  #(30.0,'USD')
    except:
        return False
    try:
        image_url = amazon_product.large_image_url
    except:
        return False
    name = amazon_product.title
    if name == None:
        return False
    asin = amazon_product.asin
    try:
        link = amazon_product._safe_get_element_text('DetailPageURL')
    except:
        return False
    product = Product(asin=asin, price=price, image_url=image_url, name=name, review="N/A", link=link)
    product.save()
    try:
        if amazon_product.features:
            features_list = amazon_product.features
            for feature in features_list:
                Feature(product=product, feature=feature).save()
        elif amazon_product.editorial_review:
            review = amazon_product.editorial_review
            product.review = review
            product.save()
    except:
        return False



    return True


def get_products_from_Amazon_update_create_product(word_list):
    #MAKE COMMENT
    products = Product.objects.all()
    for word in word_list:
        print word.name
        # new_products = amazon.search(Keywords=word.name, SearchIndex='All')
        new_products = amazon.search(Keywords=word.name, SearchIndex='Blended')
        time.sleep(0.25)
        for i, product in enumerate(new_products):
            try:
                product = Product.objects.get(asin=product.asin)
            except:
                create_product(receiver, product)
    print "end get_new_proudcts"
    return True

@login_required()
@csrf_exempt
def create_productreceiver(request, receiver_id, score, asin):
    if score == "up":
        score = 1
    else:
        score = -1
    #COMMENT HERE
    product=Product.objects.get(asin=asin)
    print product
    receiver = Receiver.objects.get(pk=int(receiver_id))
    try:
        product_receiver = ProductReceiver.objects.get(product__asin=asin, receiver=receiver)
    except ProductReceiver.DoesNotExist:
        product_receiver = ProductReceiver(product=product, receiver=receiver, score=score).save()

    #a  product has been added to the receiver list, must create and rank the words
    create_words(receiver, asin, score)

    #Returns Top 3 Ranking words
    word_list = get_top_three(receiver)

    #Search Amazon for products given word_list
    get_products_from_Amazon_update_create_product(word_list)
    return HttpResponse('true', content_type='application/json')


##################
# UPDATE HISTORY #
##################
@login_required()
@csrf_exempt
def update_history(request, receiver_id):
    print "in update_history"
    receiver = Receiver.objects.get(pk=int(receiver_id))
    products = receiver.products.all()
    data = {
        'products': products,
    }

    return render(request, "update_history.html", data)



##########################
# UPDATE RECOMMENDATIONS #
#########################
@login_required()
@csrf_exempt
def get_top_recommendations(request, receiver_id):
    # This function also seems simlar to init_receiver_page(), could make this DRYer
    print "in top_recommendations"
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
        'top_products': top_products
    }
    return render(request, "top_products.html", data)


####################
# GET NEXT PRODUCT #
####################
def get_next_product(request):
    data = {}
    all_products = Product.objects.all()
    length = len(all_products)
    product_to_rank = all_products[random.randrange(length)]
    data['product_to_rank'] = product_to_rank

    return render(request, "product_to_rank.html", data)

























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
