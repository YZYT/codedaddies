import requests
from requests.utils import requote_uri
from django.shortcuts import render
from bs4 import BeautifulSoup
import cryptography
from . import models
# Create your views here.

BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)

    final_url = BASE_CRAIGSLIST_URL.format(requote_uri(search))
    # print(final_url)
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})

    # post_title = post_listings[0].find('a', {'class':'result-title'})
    # post_url = post_listings[0].find('a', {'class':'result-title'}).get('href')
    # post_price = post_listings[0].find('span', {'class':'result-price'}).text
    # print(post_title.text)
    # print(post_url)
    # print(post_price)

    final_postings = []
    for post in post_listings:
        post_title = post.find('a', {'class': 'result-title'}).text
        post_url = post.find('a', {'class': 'result-title'}).get('href')

        if post.find('a', {'class': 'result-image'}) and post.find('a', {'class': 'result-image'}).get('data-ids'):
            post_image_url = post.find('a', {'class': 'result-image'}).get('data-ids').split(',')[0]
            post_image_url = post_image_url[2:]
            post_image_url = BASE_IMAGE_URL.format(post_image_url)
        else:
            post_image_url = 'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=2401484423,3865403126&fm=26&gp=0.jpg'

        if post.find('span', {'class': 'result-price'}):
            post_price = post.find('span', {'class': 'result-price'}).text
        else:
            post_price = 'N/A'

        final_postings.append((post_title, post_url, post_price, post_image_url))

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)