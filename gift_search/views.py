import json
from django.shortcuts import render
# import facebook
from amazon.api import AmazonAPI
# from social.backends.google import GooglePlusAuth
from demo2.settings import AMAZON_ASSOC_TAG, config, AMAZON_SECRET_KEY,AMAZON_ACCESS_KEY #SOCIAL_AUTH_GOOGLE_PLUS_KEY,
import amazonproduct
from gift_search.models import Product, WordReceiver, Receiver, ProductReceiver
import random

# plus_scope = ' '.join(GooglePlusAuth.DEFAULT_SCOPE)
amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)
receiver = None
import time


def home(request):
    # data = {
    #     "plus_scope": plus_scope,
    #     'plus_id':  SOCIAL_AUTH_GOOGLE_PLUS_KEY
    # }
    #LOGIN PAGE
    return render(request, "home.html")

def receivers(request):
    user = request.user
    receivers = user.receivers.all()
    print receivers
    data = {
        'receivers': receivers
    }
    return render(request, "receivers.html", data)

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

def receiver_page(request, receiver_id): #FINISH
    product_list = Product.objects.all()
    length = len(product_list)
    product_to_rank = product_list[random.randrange(length)]
    print product_to_rank
    # receivers_product_list = receiver.products.all()
    # while product_to_rank in receivers_product_list:
    #     rand_num = len(product_list)
    #     product_to_rank = Product.objects.get(pk=rand_num)
    # pull all products linked to receiver and put info on page
    # figure out top 3
    data = {
        'product_to_rank': product_to_rank,
    }
    return render(request, "receivers_page.html", data)


def create_words(receiver_id, asin,score):  #FINISH
    if score == "up":
        score = 1
    else:
        score = -1

    product = Product.objects.get(asin=asin)
    receiver = Receiver.objects.get(id=receiver_id)
    receiver_word_list = receiver.words
    features_list = product.features

    for feature in features_list:
        word_list = feature.split(' ')
        for word in word_list:
            if word in receiver_word_list:
                #how to change word ranking, add method to WordReceiver, this may work???
            else:
                WordReceiver(receiver=receiver, name=word,ranking=score)
    return True

def get_top_three(receiver_id):
    


def create_productreceiver(request, receiver_id, score, asin):  #FINISH and change method name
    product_receiver = ProductReceiver.objects.get(product__asin=asin,receiver__id=receiver_id)
#     do a try (if doesn't exist then use code above for product_receiver) if it does then handle error and except error raise here.
    #a  product has been added to the receiver list, must rank the words
    create_words(receiver_id,asin,score)
    get_top_three(receiver_id)
    return render(request) #WHAT ELSE???




















def get_gifts(request, receiver_id=2):
    receiver = Receiver.objects.get(pk=receiver_id)


    #ITEM LOOKUP-Python Amazon Simple Product API#
    item_ids = {'Books':'1423146735',
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
                }

    #Creates Product and Word instances for each item. Iterates through item_ids, creating products.
    # After product created, sent to create_words function to create a word instance for the features list.
    # This features list will then be incremented or decremented based on user feedback.
    products_dict = {}
    for item in item_ids:
        receiver = Receiver.objects.get(pk=receiver_id)
        product = amazon.lookup(ItemId=item_ids[item])
        features_list = product.features
        price = product.list_price[0] #(30.0,'USD')
        image_url = product.large_image_url
        name = product.title
        asin = product.asin
        # round FIGURE OUT
        product = Product(asin=asin, price=price, image_url=image_url, name=name)
        products_dict[asin]= product
        ProductReceiver(product=product,receiver=receiver)
        # round = models.IntegerField(default=None)

        create_words(features_list, receiver) #True
        time.sleep(1)

    data = {
       'products': products_dict
    } #anything else?

    print data
    return render(request, "get_gifts.html", data)

#
# def get_new_products(word):
#     products = amazon.search(Keywords=word, SearchIndex='All') #'word'
#     for i, product in enumerate(products):  #check on this
#         features_list = product.features
#         price = product.list_price[0] #(30.0,'USD')
#         image_url = product.large_image_url
#         name = product.title
#         asin = product.asin
#         # round FIGURE OUT
#         new_product = Product.objects.create(asin, price, image_url, name)
#         # round = models.IntegerField(default=None)
#
#         create_words(features_list, receiver) #True
#
#         data = {
#         'price': price,
#         'image_url': image_url,
#         'name': name,
#         'asin': asin,
#         # 'category': category
#     } #anything else?
#
#         #ajax call
#
# def gift_ranking(request, asin):
#     #look up product
#     #increment and decrement rankings
#     #word_list = find top three words, could you return as a comma deliminated string?
#     #apply weighting???
#
# #once all items are ranked (and clicked on then will need to figure out the tops three words.  Once top three words confirmed will call get_new_products




#GIFT CARD??
#maybe each offer should include a gift card at the beginning or end?






# code_snippets:
#
# get-gifts:

# #TOP SELLERS-Python Amazon Product API#
#     api = amazonproduct.API(cfg=config)
# #store itemID as string
#     result = api.item_lookup(item_id, ResponseGroup='BrowseNodes')
#     root_ids = result.xpath('//aws:BrowseNode[aws:IsCategoryRoot=1]/aws:BrowseNodeId',namespaces={'aws': result.nsmap.get(None)})
#     result = api.browse_node_lookup(root_ids[0], 'TopSellers')
# #GET ITEMS FOR BROWSE NODE, FIGURE OUT HOW TO GET ATTRIBUTES FOR CERTAIN ITEMS
#     for item in result.BrowseNodes.BrowseNode.TopSellers.TopSeller:
#         print item.ASIN, item.Title, #item.ItemAttributes.Title, item.ItemAttributes.Feature, item.Department, item.Genre, item.ListPrice, tiny_image_url???




    #features example
    #>>> product.features
# ['Stainless steel watch featuring navy dial with dual textured subdials, open lugs, and leather band with contrast stitching', 'Swiss quartz movement with analog display', 'Protective synthetic sapphire crystal dial window', 'Features buckle closure and luminous orange hands', 'Water-resistant to 165 feet (50 M): suitable for swimming and showering']
# 'Gift Card': 'B00A48G0D4',