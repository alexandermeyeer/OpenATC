#!/usr/bin/env python
from bs4 import BeautifulSoup as bs
import requests
import timeit
import time
from getconf import *

# TODO: login function, captcha

base_url = 'https://www.adidas.com'
product_id = 'BB3900'
size = '6.5'

def sleep():
	time.sleep(5)

def add_to_cart():
	response = session.get(base_url + '/us/' + product_id + '.html', headers={'Upgrade-Insecure-Requests': '1'})
	print(response)
	sleep()

	product_url = response.url

	soup = bs(response.text, 'html.parser')
	size_container = soup.find('select', {'name': 'pid'})
	size_val = 'null'

	for values in size_container.find_all('option'):
		if size == values.string.strip():
			size_val = values['value']
			break

	payload = {
		'Quantity': '1',
		'ajax': 'true',
		'layer': 'Add To Bag overlay',
		'masterPid': product_id,
		'pid': size_val
	}
	headers = {
		'Accept': '*/*',
		'Origin': 'http://www.adidas.com',
		'X-Requested-With': 'XMLHttpRequest',
	}

	if size_val != 'null':
		url = base_url + '/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-MiniAddProduct'
		response = session.post(url, data=payload, headers=headers)
		print(response)
		sleep()
		return True, product_url, size_val
	else:
		cookies = {}
		return False, product_url, size_val


def checkout():
	headers = {
		'Upgrade-Insecure-Requests': '1',
		'Referer': product_url,
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
	}
	response = session.get(base_url + '/us/delivery-start', headers=headers)
	print(response)

	sleep()

	soup = bs(response.text, 'html.parser')l
	url = soup.find('div', {'class': 'cart_wrapper rbk_shadow_angle rbk_wrapper_checkout summary_wrapper'})['data-url']
	delivery_key = soup.find('input', {'name': 'dwfrm_delivery_securekey'})['value']

	# delivery details
	headers = {
		'Accept': 'text/html, */*; q=0.01',
		'Origin': 'http://www.adidas.com',
		'X-Requested-With': 'XMLHttpRequest',
		'Referer': 'https://www.adidas.com/us/delivery-start'
	}
	payload = {
		'dwfrm_cart_selectShippingMethod': 'ShippingMethodID',
		'dwfrm_cart_shippingMethodID_0': 'Standard',
		'dwfrm_delivery_billingOriginalAddress': 'false',
		'dwfrm_delivery_billingSuggestedAddress': 'false',
		'dwfrm_delivery_billing_billingAddress_addressFields_address1': billing_address_1,
		'dwfrm_delivery_billing_billingAddress_addressFields_address2': billing_address_2,
		'dwfrm_delivery_billing_billingAddress_addressFields_city': billing_city,
		'dwfrm_delivery_billing_billingAddress_addressFields_country': billing_country_abbrv,
		'dwfrm_delivery_billing_billingAddress_addressFields_countyProvince': billing_state_abbrv,
		'dwfrm_delivery_billing_billingAddress_addressFields_firstName': first_name,
		'dwfrm_delivery_billing_billingAddress_addressFields_lastName': last_name,
		'dwfrm_delivery_billing_billingAddress_addressFields_phone': phone_number,
		'dwfrm_delivery_billing_billingAddress_addressFields_zip': billing_zip,
		'dwfrm_delivery_billing_billingAddress_isedited': 'false',
		'dwfrm_delivery_savedelivery': 'Review and Pay',
		'dwfrm_delivery_securekey': delivery_key,
		'dwfrm_delivery_shippingOriginalAddress': 'false',
		'dwfrm_delivery_shippingSuggestedAddress': 'false',
		'dwfrm_delivery_singleshipping_shippingAddress_addressFields_address1': shipping_address_1,
		'dwfrm_delivery_singleshipping_shippingAddress_addressFields_address2': shipping_address_2,
		'dwfrm_delivery_singleshipping_shippingAddress_addressFields_city': shipping_city,
		'dwfrm_delivery_singleshipping_shippingAddress_addressFields_countyProvince': shipping_state_abbrv,
		'dwfrm_delivery_singleshipping_shippingAddress_addressFields_firstName': first_name,
		'dwfrm_delivery_singleshipping_shippingAddress_addressFields_lastName': last_name,
		'dwfrm_delivery_singleshipping_shippingAddress_addressFields_phone': phone_number,
		'dwfrm_delivery_singleshipping_shippingAddress_addressFields_zip': shipping_zip,
		'dwfrm_delivery_singleshipping_shippingAddress_ageConfirmation': 'true',
		'dwfrm_delivery_singleshipping_shippingAddress_agreeForSubscription': 'false',
		'dwfrm_delivery_singleshipping_shippingAddress_email_emailAddress': email,
		'dwfrm_delivery_singleshipping_shippingAddress_isedited': 'false',
		'format': 'ajax',
		'referer': 'Cart-Show',
		'shipping-group-0': 'Standard',
		'shippingMethodType_0': 'inline',
		'signup_source': 'shipping',
		'state': shipping_state + ','
	}

	response = session.post(url, data=payload, headers=headers)
	print(response)

	# review & pay
	headers = {
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Origin': 'https://www.adidas.com',
		'X-Requested-With': 'XMLHttpRequest',
		'Referer': 'https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/COSummary-Start'
	}
	payload = {
		'dwfrm_payment_creditCard_cvn': card_cvv,
		'dwfrm_payment_creditCard_month': card_exp_month,
		'dwfrm_payment_creditCard_number': card_number,
		'dwfrm_payment_creditCard_owner': '{} {}'.format(first_name, last_name),
		'dwfrm_payment_creditCard_type': '001',  # visa
		'dwfrm_payment_creditCard_year': card_exp_year,
		'dwfrm_payment_securekey': delivery_key,
		'dwfrm_payment_signcreditcardfields': 'sign'
	}

	url = soup.find('form', {'id': 'dwfrm_delivery'})['action']
	response = session.post(url, data=payload, headers=headers)
	print(response)


# Main
start = timeit.default_timer()
session = requests.Session()
session.headers.update({
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
	              'Chrome/52.0.2743.116 Safari/537.36',
	'DNT': '1',
	'Accept-Encoding': 'gzip, deflate, sdch',
	'Accept-Language': 'en-US,en;q=0.8,da;q=0.6',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
})

successful, product_url, size_val = add_to_cart()

if successful:
	checkout()

print(timeit.default_timer()-start)


