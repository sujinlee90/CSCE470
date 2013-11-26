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
	    self.users = {}
    	#List of the names of the JSON files containing the tweets about the TV shows
	    ### Maybe this list needs to be updated
	    self.list_tvshows = ["AmericanHorrorStory.json","Arrow.json","BreakingBad.json","Dracula.json","GameOfThrones.json","HowIMetYourMother.json","OnceUponATime.json","OrangeIsTheNewBlack.json","TheWalkingDead.json","TheBigBangThoery.json","TheVampireDiaries.json","Homeland.json","ModernFamily.json","GraysAnatomy.json","DoctorWho.json","PrettyLittleLiars.json","SonsOfAnarchy.json","Supernatural.json","AgentsOfSHIELD.json","TheBlacklist.json","TheOriginals.json","BoardwalkEmpire.json","Ravenswood.json","Revolution.json","Reign.json","Revenge.json","MastersOfSex.json","WitchesOfEastEnd.json","SleepyHollow.json","TrueDetective.json","Sherlock.json","Dexter.json","Bones.json","TheMentalist.json","Glee.json","NCIS.json","DowntonAbbey.json","OnceUponATimeInWonderland.json","Castle.json","TheCarrieDiaries.json","TrueBlood.json","Suits.json","Scandal.json","NewGirl.json","UnderTheDome.json","PersonOfInterest.json","CriminalMinds.json","WhiteCollar.json","TheTomorrowPeople.json"]
	    self.sum_tvshows = [0]*50
	
	def process_tweets(self, data, index):
	    for tweets in data:
		for tweet in tweets:
		    username = tweet['user']
			#If the user is not in the users list yet, add the user to
			#the dictionary (using the username as token and creating a
			#vector that will store the number of tweets the user posted
			#about each TV show.
			if username not in self.users:
			    self.users[username] = [0]*50
                        #Adding a mention to the respective TV show (indicated by the index)
			self.users[username][index] += 1
		
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
		
	    for tv_show in self.list_tvshows:
		#Extracting the tweets from the json file
		tweets = read_data(tv_show)
		print "Number of tweets: ", len(tweets)
		
		tweets_count.append(len(tweets))
			
		#Calculating the index of the TV show
		index += 1
			
		process_tweets(tweets, index)
		
	    #Creating a vector (Python list) to store the number of
	    #different TV shows each user mentioned
	    number_dif_tvshows = [0]*len(self.users) 
	    i = 0
	    #For each user, calculate the number of different TV shows his/her tweets mention
	    for user in self.users:
		number_dif_tvshows[i] = count_dif_tvshows(self.users[user])
		i += 1
		
	    #Creating a vector (Python list) to store the number of
	    #different users that mentioned n different TV shows
	    #Example: if number_users_n_dif_tvshows[3] = 100, it means
	    #that 100 users twitted about 3 different TV shows
	    number_users_n_dif_tvshows = [0]*len(self.list_tvshows)	
	    for user in self.users:
		number_users_n_dif_tvshows[count_dif_tvshows(self.users[user])] += 1

	    print 'Number of users: ', len(self.users)
	    print number_users_n_dif_tvshows
		
	    #Saving the data in a file
	    datas = [tweets_count, number_dif_tvshows]
	    f = open('results.txt', 'w')
	    json.dump(datas, f )

	def make_sum_table(self, tv_show):
            """
            This function used to find users who mentioned same tv show as the user and mentioned other tv shows.
            Then, sum all counts from the users.
            """
            #find index for tv show the user searches
            tv_show_index = self.list_tvshows.index(tv_show)

            #find user who mentioned the tv show and mentioned more than or equal to two tv shows
            for user in self.users:
                if self.users[tv_show_index] != 0:
                    if count_dif_tvshows(self.users[user]) > 1:
                        for i in range(0, len(self.list_tvshows)):
                            self.sum_tvshows[i] = self.sum_tvshows[i] + self.users[user][i]

        def print_user_mentions_tvshow(self, tv_show1, tv_show2, count):
            """
            find users who mention both tv_show1 and tv_show2 and print the users' mention
            count is the number of user
            """
            the_number_of_users = 0
            tv_show1_index = self.list_tvshows.index(tv_show1)
            tv_show2_index = self.list_tvshows.index(tv_show2)

            while(the_number_of_users < count):
                for user in self.users:
                    if (self.users[tv_show1_index] != 0) & (self.users[tv_show2_index] != 0):
                        print 'User:', user, ', Text:' # need to find text

        def recommend_tvshows(self, tv_show):
            """
            make TV show ranking
            """
            #build tv show dictionary for making easy to sort
            dic_tvshows = {}
            for n in range(0, len(self.list_tvshows)):
                dic_tvshows[self.list_tvshows[n]] = self.sum_tvshows[n]

            #sort tv shows by reverse order
            sorted_tvshows = sorted(dic_tvshows.iteritems(), key = operator.itemgetter(1), reverse = True)

            #save top 5 tv shows
            top_5_tvshows = shorted_tvshows[:5]
            
            #find users who mentioned tv shows in ranking top 5 and print users' text
            print_user_mentions_tvshow(tv_show, top_5_tvshows.keys()[0]) #print users' mention for top 1
            print_user_mentions_tvshow(tv_show, top_5_tvshows.keys()[1]) #print users' mention for top 2
            print_user_mentions_tvshow(tv_show, top_5_tvshows.keys()[2]) #print users' mention for top 3
            print_user_mentions_tvshow(tv_show, top_5_tvshows.keys()[3]) #print users' mention for top 4
            print_user_mentions_tvshow(tv_show, top_5_tvshows.keys()[4]) #print users' mention for top 5
            
		
if __name__ == "__main__":
	rec = Recommender()
	rec.index_tweets()
