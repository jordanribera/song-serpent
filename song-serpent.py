#!/usr/bin/env python

import tweepy
import json
import os.path

def is_mention(word):
	if word.startswith("@"):
		return True
	return False

def is_link(word):
	if word.startswith("http"):
		return True
	if word.startswith("https"):
		return True
	return False

def clean_tweet(original_text):
	words = original_text.split()
	bad_words = []
	#print "CHECKING: " + original_text
	for word in words:
		#print "    WORD: " + word
		if is_mention(word):
			#print "        is a mention"
			bad_words.append(word)
		if is_link(word):
			#print "        is a link"
			bad_words.append(word)
	for bad_word in bad_words:
		words.remove(bad_word)

	output = " ".join(words)
	#print "    OUTPUT: " + output
	return output

if __name__ == "__main__":

	# load config
	if os.path.isfile("credentials.json"):
		try:
			with open ("credentials.json", "r") as f:
				credentials = json.load(f)
		except ValueError:
			print "credentials.json is malformed."
			exit()
	else:
		empty_credentials = {u'consumer-key': u'', u'consumer-secret': u'', u'access-token': u'', u'access-token-secret': '', u'user-name': u''}
		with open ("credentials.json", "w") as f:
			json.dump(empty_credentials, f, indent=4, separators=(',', ':'))
		print "credentials.json is missing. i've created a blank one for you."
		exit()

	# authenticate
	auth = tweepy.OAuthHandler(credentials["consumer-key"], credentials["consumer-secret"])
	auth.set_access_token(credentials["access-token"], credentials["access-token-secret"])

	# connect to the api
	api = tweepy.API(auth)

	#show my tweets
	try:
		my_tweets = api.user_timeline(credentials["user-name"], count=100)
		for tweet in my_tweets:
			print clean_tweet(tweet.text)
	except:
		print "there was a problem fetching tweets. check your credentials."