#!/usr/bin/env python

import sys

import tweepy
import json
import os.path
import redis
from markov import Markov

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

	#output = " ".join(words)
	#print "    OUTPUT: " + output
	return words

def index_feed(target):
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

	#add tweets to redis
	tweet_data = Markov(target)

	#show my tweets
	try:
		my_tweets = api.user_timeline(target, count=20000)
		for tweet in my_tweets:
			cleaned_tweet = clean_tweet(tweet.text)
			tweet_string = " ".join(cleaned_tweet)
			print 'indexing tweet: "' + tweet_string + '"'
			tweet_data.add_line_to_index(cleaned_tweet)
	except Exception as e:
		print e

def make_tweet(target):
	target_data = Markov(target)

	output_tweet = target_data.generate(max_words=10)
	return output_tweet

if __name__ == "__main__":

	if len(sys.argv) < 2:
		print "tell me what to do..."
		exit()
	else:
		operation = sys.argv[1]

		if operation == 'index':
			target = sys.argv[2]

			index_feed(target)
			exit()

		if operation == 'tweet':
			target = sys.argv[2]

			print make_tweet(target)
			exit()