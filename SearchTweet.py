#!/usr/bin/env python
# -*- coding: utf-8  -*-
#encoding=utf-8

import tweepy
import json
import os
consumer_key = 'EcRzLcaJLht0yHI87W5vg'
consumer_secret = 'axM88WFwSxxBXna9myheIH7LAIzaxzxXZruMRiZM'
access_token_key = '992311357-NLEJvR6XeestU9aTRUYtJ6MhwZPIXT8F676MiV7l'
access_token_secret = 'EB3SubIXk3CL3dz01sCdZw2hEwoEarU7o0xZBAo'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)

with open('TheBigBangTheory.json', 'w') as outfile:
        result = []
        #for its_list in tv_list:
	
	#list = api.search(dat)
        for tweet in tweepy.Cursor(api.search,q= "big bang theory",geocode='30.2395,-97.8387,100mi', count =100,result_type="recent", include_entities=True,lang="en").items():
                data = {}
                data["user"] = tweet.user.screen_name
                data["id"] = tweet.id
                data["text"] = tweet.text.encode('utf-8')
                #data["entities"] = tweet.entities
                result.append(data)
                #print result
                #print tweet.user.screen_name
        json.dump(result, outfile)
        print len(result)
