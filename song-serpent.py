#!/usr/bin/env python

import tweepy
import json

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
	with open ("credentials.json", "r") as f:
		credentials = json.load(f)

	# authenticate
	auth = tweepy.OAuthHandler(credentials["consumer-key"], credentials["consumer-secret"])
	auth.set_access_token(credentials["access-token"], credentials["access-token-secret"])

	# connect to the api
	api = tweepy.API(auth)

	#show my tweets
	my_tweets = api.user_timeline(credentials["user-name"], count=100)
	for tweet in my_tweets:
		print clean_tweet(tweet.text)