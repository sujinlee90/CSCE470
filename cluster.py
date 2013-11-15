from __future__ import division
import re
from stemming import porter2
import math
import json
import os
import collections
from operator import itemgetter

users={}

def dictionary_list(tweets, index,counts):
		for twt in tweets:
			print len(twt)
			counts =counts+len(twt)
			print counts
			for data in twt:
				username = data['user']
				if username not in users:
					users[username] = [0]*50
				users[username][index] += 1
		return counts
				
def tokenize(text):
    """
    Take a string and split it into tokens on word boundaries.
      
    A token is defined to be one or more alphanumeric characters,
    underscores, or apostrophes.  Remove all other punctuation, whitespace, and
    empty tokens.  Do case-folding to make everything lowercase. This function
    should return a list of the tokens in the input string.
    """
    tokens = re.findall("[\w']+", text.lower())
    return [porter2.stem(token) for token in tokens]
	
	
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
        print "Failed to read data!"
        return []
    print "The json file has been successfully read!"
    return data

def dif_tvshows(list):
	n = 0
	for count in list:
		if count > 0:
			n += 1
	return n

class Cluster():
	def __init__(self):
    	# put your final clustering results 
    	# in the variable self.results with the format
    	# {index of cluster: [tweet_id]} 
    	# e.g. {1:[122312312,3421421231], 2:[87862321,2121321986],...}
		self.results = {}
	
	

		
	def index_tweets(self):
		
		data = []
		data1=[]
		tv_show={}
		index = 0
		list
		"""
		read_tvshows = read_data('jsonfiles.json')
		
		print read_tvshows['tvshows']
	"""
	
		list_tvshows= ["AgentsOfShield.json", "AmericanHorrorStory.json", "Arrow.json", "BoardWalkEmpire.json", "Castle.json", "CriminalMinds.json", "Dexter.json", "DoctorWho.json", "DowntonAbbey.json", "GameOfThrones.json", "Glee.json", "GraysAnatomy.json", "HowIMetYourMother.json", "MastersOfSex.json", "ModernFamily.json", "NCIS.json", "NewGirl.json", "OnceUponATime.json", "OnceUponATimeInWonderland.json", "OrangeIsTheNewBlack.json", "PersonOfInterest.json", "PrettyLittleLiars.json", "Ravenswood.json", "Reign.json, Revenge.json", "Revolution.json", "Scandal.json", "Sherlock.json", "SleepyHollow.json", "SonsOfAnarchy.json", "Suits.json", "Supernatural.json", "TheBigBangTheory.json", "TheBlacklist.json", "TheCarrieDiaries.json", "TheMentalist.json", "TheOriginals.json", "TheTomorrowPeople.json", "TheVampireDiaries.json", "TheWalkingDead.json", "TrueBlood.json", "TrueDetective.json", "UnderTheDome.json", "WhiteCollar.json", "WitchesOfEastEnd.json"]
		
		
		temp =["AmericanHorrorStory.json","Arrow.json","BreakingBad.json","Dracula.json","GameOfThrones.json","HowIMetYourMother.json","OnceUponATime.json","OrangeIsTheNewBlack.json","TheWalkingDead.json","TheBigBangThoery.json","TheVampireDiaries.json","Homeland.json","ModernFamily.json","GraysAnatomy.json","DoctorWho.json","PrettyLittleLiars.json","SonsOfAnarchy.json","Supernatural.json","AgentsOfSHIELD.json","TheBlacklist.json","TheOriginals.json","BoardwalkEmpire.json","ravenswood.json","Revolution.json","Reign.json","Revenge.json","MastersOfSex.json","WitchesOfEastEnd.json","SleepyHollow.json","TrueDetective.json","Sherlock.json","Dexter.json","Bones.json","TheMentalist.json","Glee.json","NCIS.json","DowntonAbbey.json","OnceUponATimeInWonderland.json","Castle.json","TheCarrieDiaries.json","TrueBlood.json","Suits.json","Scandal.json","NewGirl.json","UnderTheDome.json","PersonOfInterest.json","CriminalMinds.json","WhiteCollar.json","TheTomorrowPeople.json"]
		tweets_count = []
		counts=0
		for x in temp:
			print x
			tweets=read_data(x)
			print "len" ,len(tweets)
			
			tweets_count.append(len(tweets))
			index+=1
			counts = dictionary_list(tweets,index,counts)
		
			
			
		dif_count = [0]*len(users) 
		i = 0
		for user in users:
			dif_count[i] = dif_tvshows(users[user])
			i += 1
			
		users_dif_count = [0]*50 		
		for user in users:
			users_dif_count[dif_tvshows(users[user])] += 1

		
		
		print 'users', len(users)
		print users_dif_count
		
		datas =[tweets_count, dif_count]
		print counts , "data"
		f = open('data1.txt', 'w')
		
		json.dump(datas, f )
		
		
				
				
				
	
			
			
			
				
		
		
		
		
	
		
		
		#print final_list1
        
if __name__ == "__main__":
	api= Cluster()
	api.index_tweets()
        