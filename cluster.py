from __future__ import division
import re
from stemming import porter2
import math
import json
import os
import collections
from operator import itemgetter
	
def read_data(filename):
    """
    Used to read all tweets from the json file.
    """
    data = []
    try:
        with open(filename) as f:
            for line in f:
                data.append(json.loads(line.strip()))
    except:
        print filename, ": Failed to read data!"
        return []
    print "The json file has been successfully read!"
    return data

class Recommender():
	def __init__(self):
		users = {}
    	#List of the names of the JSON files containing the tweets about the TV shows
		### Maybe this list needs to be updated
		list_tvshows = ["AmericanHorrorStory.json","Arrow.json","BreakingBad.json","Dracula.json","GameOfThrones.json","HowIMetYourMother.json","OnceUponATime.json","OrangeIsTheNewBlack.json","TheWalkingDead.json","TheBigBangThoery.json","TheVampireDiaries.json","Homeland.json","ModernFamily.json","GraysAnatomy.json","DoctorWho.json","PrettyLittleLiars.json","SonsOfAnarchy.json","Supernatural.json","AgentsOfSHIELD.json","TheBlacklist.json","TheOriginals.json","BoardwalkEmpire.json","Ravenswood.json","Revolution.json","Reign.json","Revenge.json","MastersOfSex.json","WitchesOfEastEnd.json","SleepyHollow.json","TrueDetective.json","Sherlock.json","Dexter.json","Bones.json","TheMentalist.json","Glee.json","NCIS.json","DowntonAbbey.json","OnceUponATimeInWonderland.json","Castle.json","TheCarrieDiaries.json","TrueBlood.json","Suits.json","Scandal.json","NewGirl.json","UnderTheDome.json","PersonOfInterest.json","CriminalMinds.json","WhiteCollar.json","TheTomorrowPeople.json"]
	
	def process_tweets(self, data, index):
		for tweets in data:
			for tweet in tweets:
				username = tweet['user']
				#If the user is not in the users list yet, add the user to
				#the dictionary (using the username as token and creating a
				#vector that will store the number of tweets the user posted
				#about each TV show.
				if username not in users:
					users[username] = [0]*50
				#Adding a mention to the respective TV show (indicated by the index)
				users[username][index] += 1
		
	#Count the number of different TV shows that were cited on the list of tweets
	#from a certain user. The parameter passed to the function is a vector with the
	#number of tweets for each TV show.
	def count_dif_tvshows(list):
		n_tvshows = 0
		#count is the number of tweets about a certain TV show
		for count in list:
			#if count > 0, it means that the user mentioned the TV show at least once
			#if not, it means that there is no tweet about that TV show posted by this user
			if count > 0:
				n_tvshows += 1
		return n_tvshows
	
	def index_tweets(self):
		index = 0	#Index number of the TV show on the list

		tweets_count = []	#Number of tweets for each TV show
		
		for tv_show in list_tvshows:
			#Extracting the tweets from the json file
			tweets = read_data(tv_show)
			print "Number of tweets: ", len(tweets)
			
			tweets_count.append(len(tweets))
			
			#Calculating the index of the TV show
			index += 1
			
			process_tweets(tweets, index)
		
		#Creating a vector (Python list) to store the number of
		#different TV shows each user mentioned
		number_dif_tvshows = [0]*len(users) 
		i = 0
		#For each user, calculate the number of different TV shows his/her tweets mention
		for user in users:
			number_dif_tvshows[i] = count_dif_tvshows(users[user])
			i += 1
		
		#Creating a vector (Python list) to store the number of
		#different users that mentioned n different TV shows
		#Example: if number_users_n_dif_tvshows[3] = 100, it means
		#that 100 users twitted about 3 different TV shows
		number_users_n_dif_tvshows = [0]*len(list_tvshows)	
		for user in users:
			number_users_n_dif_tvshows[count_dif_tvshows(users[user])] += 1

		print 'Number of users: ', len(users)
		print number_users_n_dif_tvshows
		
		#Saving the data in a file
		datas = [tweets_count, number_dif_tvshows]
		f = open('results.txt', 'w')
		json.dump(datas, f )

		
if __name__ == "__main__":
	rec = Recommender()
	rec.index_tweets()