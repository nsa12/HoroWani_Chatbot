#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import requests
import re

# Create your views here.

VERIFY_TOKEN = 'HoroscopeBot'
PAGE_ACCESS_TOKEN = 'EAAFG7c6eT2UBAKcP1QRPyWMBZAZA37Um3zNoQ3jFYm4KCDAdRxhV3CgQTaSoAlAcQsu6XWoa4cM7wC2NtKatCsETNweF5MjARiyPEdZAwKSry2ZCZC6hIFCcSC7sdAL9UH6rd8rLOcwKGxLXuEFoesECj39Jv7XFdRBZC3qUOZCZAAZDZD'

def index(request):
	return HttpResponse('Horoscope Bot Page')

class MyChatBotView(generic.View):
	def get (self, request, *args, **kwargs):
		if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Whoops. Invalid token')

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		incoming_message= json.loads(self.request.body.decode('utf-8'))

		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				print message
				try:
					sender_id = message['sender']['id']
					message_text = message['message']['text']
					post_facebook_message(sender_id,message_text)
				except Exception as e:
					print e
					pass
		return HttpResponse()

def post_facebook_message(fbid, message_text):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	
	output_text = getHoro(output_text)
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":output_text}})
	
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	print status.json()

def getHoro(text):
	url = 'http://horoscope-api.herokuapp.com/horoscope'
	text = text.lower()

	time = 'today'
	if 'week' in text:
		time = 'week'
	elif 'month' in text:
		time = 'month'
	elif 'year' in text:
		time = 'year'

	if 'aries' in text:
		zodiac = 'aries'
	elif 'taurus' in text:
		zodiac = 'taurus'
	elif 'gemini' in text:
		zodiac = 'gemini'
	elif 'cancer' in text:
		zodiac = 'cancer'
	elif 'leo' in text:
		zodiac = 'leo'
	elif 'virgo' in text:
		zodiac = 'virgo'
	elif 'libra' in text:
		zodiac = 'libra'
	elif 'scorpio' in text:
		zodiac = 'scorpio'
	elif 'sagittarius' in text:
		zodiac = 'sagittarius'
	elif 'capricorn' in text:
		zodiac = 'capricorn'
	elif 'aquarius' in text:
		zodiac = 'aquarius'
	elif 'pisces' in text:
		zodiac = 'pisces'
	else:
		return 'Sorry. Your sunsign wasn\'t found. Please try again.'
	
	url = url + '/' + time + '/' + zodiac
	r = requests.get(url=url)
	data = r.json()
	scoped_data = str(data['horoscope'])

	if len(scoped_data) > 315:
		scoped_data = scoped_data[:315] + '...'

	return scoped_data