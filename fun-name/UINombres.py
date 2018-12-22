#!/usr/bin/env python3
#
# Client for the UINames.com service.
#
# 1. Decode the JSON data returned by the UINames.com API.
# 2. Print the fields in the specified format.
#
# Example output:
# My name is Tyler Hudson and the PIN on my card is 4840.

import requests

def SampleOutput():
	# decode JSON data with chosen region
	person1 = requests.get('https://uinames.com/api?ext&region=morocco')

	# create variables for specified output format
	name = person1.json()['name']
	surname = person1.json()['surname']
	pin = person1.json()['credit_card']['pin']

	# return specified message
	return("My name is {} {} and the PIN on my card is {}".format(name, surname, pin))

if __name__ == '__main__':
	print(SampleOutput())