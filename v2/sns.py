#!/usr/bin/python3
import sys
import requests
import timeit
import traceback
from checkoutconf import *
from bs4 import BeautifulSoup as bs
'''
####
#
# Sneakersnsstuff auto-copper. Will add payment details loaded from a config file.
#
# Authored by: am3y
####
'''

early_bird = ''

def sneak_finder(description):
    print("Based on the given input I can match the sneaker you are looking for")
    return 0

base_url = "http://www.sneakersnstuff.com/en/"

def addToCart(url,size):

    size_code = ''
    session = requests.Session()
    #print(repr(session)) ##

    response = session.get(base_url + url)
    #print(repr(response.text))

    if (response.status_code == 200):
        print("URL OK...")
        soupMe = bs(response.text, 'html.parser')
        form = soupMe.find('form', { 'id': 'add-to-cart-form' })
        size_divs = form.find_all('div', { 'class':  'size-button property available'})
        print('Number of sizes found: {}'.format(len(size_divs)))
        anti_token = form.find('input', {'name': '_AntiCsrfToken'})['value']

        for x in size_divs:
            if(x.text.strip().replace('US ', '')  === size):
                print("Bingo!")
                break
            else:
                print("Size not available")
                return

        payload = {
            '_AntiCsrfToken' : anti_token,
            'partial': 'cart-summary',
            'id' : size_code
        }

    else:
        print("  - ERROR - Check if URL is valid in your browser")

    return 0



addToCart(sys.argv[1],sys.argv[2])
