from __future__ import division
import re
import math
import json
import os
import operator
import imdb

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
    #print "The json file has been successfully read!"
    return data

class Recommender():
    def __init__(self):
        self.users = {}
        #List of the names of the JSON files containing the tweets about the TV shows
        ### Maybe this list needs to be updated
        data = read_data("tv_shows_info.json")
        self.tv_shows_info = data[0]
        self.list_tvshows = []
        for tvshow in self.tv_shows_info:
            self.list_tvshows.append(tvshow["title"])
        #self.list_tvshows = ["AmericanHorrorStory.json","Arrow.json","BreakingBad.json","Dracula.json","GameOfThrones.json","HowIMetYourMother.json","OnceUponATime.json","OrangeIsTheNewBlack.json","TheWalkingDead.json","TheBigBangTheory.json","TheVampireDiaries.json","Homeland.json","ModernFamily.json","GraysAnatomy.json","DoctorWho.json","PrettyLittleLiars.json","SonsOfAnarchy.json","Supernatural.json","AgentsOfSHIELD.json","TheBlacklist.json","TheOriginals.json","BoardwalkEmpire.json","Ravenswood.json","Revolution.json","Reign.json","Revenge.json","MastersOfSex.json","WitchesOfEastEnd.json","SleepyHollow.json","TrueDetective.json","Sherlock.json","Dexter.json","Bones.json","TheMentalist.json","Glee.json","NCIS.json","DowntonAbbey.json","Castle.json","TheCarrieDiaries.json","TrueBlood.json","Suits.json","Scandal.json","NewGirl.json","UnderTheDome.json","PersonOfInterest.json","CriminalMinds.json","WhiteCollar.json","TheTomorrowPeople.json"]
        
        data = read_data("tv_shows_detailed.json")
        self.tv_shows_detailed = data[0][0]
        
        self.sum_tvshows = [0]*len(self.list_tvshows)
        self.tweet_text = {}
    
    def process_tweets(self, data, index):
        for tweets in data:
            for tweet in tweets:
                username = tweet['user']
                #If the user is not in the users list yet, add the user to
                #the dictionary (using the username as token and creating a
                #vector that will store the number of tweets the user posted
                #about each TV show.
                if username not in self.users:
                    self.users[username] = [0]*len(self.list_tvshows)
                #Adding a mention to the respective TV show (indicated by the index)
                self.users[username][index] += 1
                text = tweet['text']
                if not self.tweet_text.has_key(index):
                    self.tweet_text[index] = []
                self.tweet_text[index].append({'user':username,'text':text})
                        
        
    #Count the number of different TV shows that were cited on the list of tweets
    #from a certain user. The parameter passed to the function is a vector with the
    #number of tweets for each TV show.
    def count_dif_tvshows(self, list):
        n_tvshows = 0
        #count is the number of tweets about a certain TV show
        for count in list:
            #if count > 0, it means that the user mentioned the TV show at least once
            #if not, it means that there is no tweet about that TV show posted by this user
            if count > 0:
                n_tvshows += 1
        return n_tvshows
    
    def index_tweets(self, location):
        index = 0    #Index number of the TV show on the list

        tweets_count = []    #Number of tweets for each TV show
        
        for tv_show in self.list_tvshows:
            #Extracting the tweets from the json file
            tweets = read_data(self.get_folder_name(location) + self.get_file_name(tv_show))
        
            tweets_count.append(len(tweets))
            
            self.process_tweets(tweets, index)
                
            #Calculating the index of the TV show
            index += 1
        
        #Creating a vector (Python list) to store the number of
        #different TV shows each user mentioned
        number_dif_tvshows = [0]*len(self.users) 
        i = 0
        #For each user, calculate the number of different TV shows his/her tweets mention
        for user in self.users:
            number_dif_tvshows[i] = self.count_dif_tvshows(self.users[user])
            i += 1
        
        #Creating a vector (Python list) to store the number of
        #different users that mentioned n different TV shows
        #Example: if number_users_n_dif_tvshows[3] = 100, it means
        #that 100 users twitted about 3 different TV shows
        number_users_n_dif_tvshows = [0]*len(self.list_tvshows)
        for user in self.users:
            number_users_n_dif_tvshows[self.count_dif_tvshows(self.users[user])] += 1

        #print 'Number of users: ', len(self.users)
        #print number_users_n_dif_tvshows
        
        """
        #Saving the data in a file
        datas = [self.users]
        f = open('results.txt', 'w')
        json.dump(datas, f )
        """

    def make_sum_table(self, tv_show):
        """
        This function used to find users who mentioned same tv show as the user and mentioned other tv shows.
        Then, sum all counts from the users.
        """
        #find index for tv show the user searches
        tv_show_index = self.list_tvshows.index(tv_show)
        print  "tv_show_index = ", tv_show_index, tv_show

        #find user who mentioned the tv show and mentioned more than or equal to two tv shows
        for user, tv_show_n_mentions in self.users.iteritems():
            if tv_show_n_mentions[tv_show_index] != 0:
                if self.count_dif_tvshows(tv_show_n_mentions) > 1:
                    for i in range(0, len(self.list_tvshows)):
                        self.sum_tvshows[i] = self.sum_tvshows[i] + tv_show_n_mentions[i]

    def get_user_mentions_tvshow(self, tv_show):
        """
        find users who mention both tv_show and print the users' mention
        count is the number of user
        """
        the_number_of_users = 0
        tvshow_index = self.list_tvshows.index(tv_show)
        result = []
        # print 10 users who mentioned the tv show
        for i in range(0,10):
            result.append('User:' + self.tweet_text[tvshow_index][i]['user'] + ', Text:' + self.tweet_text[tvshow_index][i]['text'].encode('utf-8'))
        return result

    def get_folder_name(self, location):
        return {
            "NY": "./NewYork_tweets/",
            "LA": "./LosAngeles_tweets/",
            "CH": "./Chicago_tweets/",
            "HO": "./Houston_tweets/",
            "PH":  "./Philadelphia_tweets/",
            }.get(location, "./Chicago_tweets/")
            
    def get_file_name(self, tv_show):
        index = self.list_tvshows.index(tv_show)
        return self.tv_shows_info[index]["file_name"]
     
    def get_tv_show_info(self, tvshow_id, file_name):
        access = imdb.IMDb()
        movie = access.get_movie(tvshow_id)
        small_cover = "./Pictures/" + file_name.replace(" ", "") + "_small.jpg"
        big_cover = "./Pictures/" + file_name.replace(" ", "") + "_big.jpg"
        return {"title": movie['title'], "year": movie['year'], "genres": movie['genres'], "plot": movie['plot outline'], "small_cover": small_cover, "big_cover": big_cover}
        #return {"title": movie['title'], "year": movie['year'], "genres": movie['genres'], "plot": movie['plot outline'], "small_cover": movie['cover url'], "big_cover": movie['full-size cover url']}
            
    def recommend_tvshows(self, tv_show, location):
        """
        make TV show ranking
        """

        self.index_tweets(location)
        self.make_sum_table(tv_show)
        
        #build tv show dictionary for making easy to sort
        dic_tvshows = {}
        for n in range(0, len(self.list_tvshows)):
            dic_tvshows[self.list_tvshows[n]] = self.sum_tvshows[n]

        #Remove the searched TV show from the results list
        del dic_tvshows[tv_show]
        
        #sort tv shows by reverse order
        sorted_tvshows = list(sorted(dic_tvshows, key = dic_tvshows.__getitem__, reverse = True))
        
        print "\nTop 5 TV shows recommended for Breaking Bad with the number of users that talked about that TV show and Breaking Bad:"
        for item in enumerate(sorted(dic_tvshows.iteritems(), key = operator.itemgetter(1), reverse = True)[:5]):
            print item
        print "\nSome tweets about the first TV show:\n"
        
        #find users who mentioned tv shows in ranking top 5 and print users' text
        print self.get_user_mentions_tvshow(sorted_tvshows[0]) #print users' mention for top 1
        
        index = self.list_tvshows.index(sorted_tvshows[0])
        #print self.get_tv_show_info(self.tv_shows_info[index]["id"])#self.tv_shows_info[index]["id"])
        #self.print_user_mentions_tvshow(sorted_tvshows.keys()[1]) #print users' mention for top 2
        #self.print_user_mentions_tvshow(sorted_tvshows.keys()[2]) #print users' mention for top 3
        #self.print_user_mentions_tvshow(sorted_tvshows.keys()[3]) #print users' mention for top 4
        #self.print_user_mentions_tvshow(sorted_tvshows.keys()[4]) #print users' mention for top 5
        
        #Returning the list of recommended TV shows
        result = []
        for item in enumerate(sorted(dic_tvshows.iteritems(), key = operator.itemgetter(1), reverse = True)[:5]):
            result.append(item[1][0])
        result_list = []
        
        
        #Creating a json file with the detailed info about all the TV shows
        """
        for r in self.list_tvshows:
            index = self.list_tvshows.index(r)
            file_name = self.get_file_name(r)
            result_list.append(self.get_tv_show_info(self.tv_shows_info[index]["id"], file_name))
        datas = [result_list]
        f = open('results.txt', 'w')
        json.dump(datas, f )
        """
        
        for r in result:
            index = self.list_tvshows.index(r)
            result_list.append(self.tv_shows_detailed[index])
        
        return result_list
         
if __name__ == "__main__":
    rec = Recommender()
    print rec.recommend_tvshows("Breaking Bad", "NY")
