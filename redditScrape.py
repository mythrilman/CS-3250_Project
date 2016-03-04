import requests
import praw
import json
import csv
import time
from time import gmtime, strftime

#out hand selected list of subreddits to study
subredditArray = ["politics", "AdviceAnimals", "DotA2", "nba", "WTF", "relationships", "BlackPeopleTwitter", "RocketLeague", "gamephysics", "gonewild", "memes", "astrophotography", "bloodborne", "ShitRedditSays", "RandomActsOfBlowJob", "AskScienceFiction", "arduino", "pathofexile", "swtor", "boobbounce", "Ubuntu", "NSFW_Snapchat", "EverythingScience", "KotakuInAction", "arrow", "StarWarsBattlefront", "badhistory", "snowboarding", "HomeImprovement", "lifeofnorman", "economy", "SWARJE", "illusionporn", "torrents", "runescape", "musictheory", "funhaus", "camwhores", "privacy", "Eve", "BeAmazed", "TheGirlSurvivalGuide", "amiugly", "waterporn", "swoleacceptance", "Offensive_Wallpapers", "Cynicalbrit", "audiophile", "TheoryOfReddit", "Jazz", "Aquariums"]

#open csv file for the front page
frontPageReview = open('front_page_data.csv', 'wb')
frontReview = csv.writer(frontPageReview, delimiter=",")
frontReview.writerow(["Date/Time",1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25])	

#make array for the first row using the subreddit array
firstRowArray = []
firstRowArray.append("Date/Time")
for sub in subredditArray:
	firstRowArray.append(sub)

#make csv files for subscribers and active users and write the first row for each
subscriberData = open('subscriber_data.csv', 'wb')
subscriberReview = csv.writer(subscriberData, delimiter=",")

activeData = open('active_user_data.csv', 'wb')
activeReview = csv.writer(activeData, delimiter=",")
subscriberReview.writerow(firstRowArray)
activeReview.writerow(firstRowArray)

#function for gathering data using all other functions here
def gather_reddit_data(iterations):
	import time
	#loop though waiting 15 minutes each time for iterations times
	for x in range(0, iterations):
		currentTime = strftime("%Y-%m-%d %H:%M", gmtime())
		print "STARTING ROW " + currentTime + "\n" 
		write_front_page_row(currentTime)
		write_subscribe_row(currentTime)
		write_active_row(currentTime)
		#Delay 15 Minutes
		print "DING\n"
		time.sleep(900)

	frontPageReview.close()
	subscriberData.close()
	activeData.close()

#this function gets the active users of a subreddit using json
def get_active_users(subreddit):
    url = "http://www.reddit.com/r/{}/about.json".format(subreddit)
    headers = {"User-Agent": "School Project"}
    resp = requests.get(url, headers=headers)
    if not resp.ok:
        # handle request error, return -1?
        return -1
    content = resp.json()
    return content["data"]["accounts_active"]

#this function gets the subscriber count of a subreddit using praw
def get_subscribers(subreddit):
	r = praw.Reddit("School Project")
	try:
		return r.get_subreddit(subreddit).subscribers
	except Exception, e:
		return -1
#this function gets the current posts on top of r/all using praw
def get_front_page():
	r = praw.Reddit("School Project")
	subArray = []
	try:
		posts = r.get_subreddit('all').get_hot(limit = 25)
		for post in posts:
			subArray.append(post.subreddit)
	except Exception, e:
		for x in range(1,26):
			subArray.append("N/A")
	return subArray

#this function writs the top posts on r/all to the frontReview csv file
def write_front_page_row(time):
	#create empty array
	subArray = []
	#put the current time/date in the first index
	subArray.append(time)
	#run through the front page and append every entry to the array
	for post in get_front_page():
		subArray.append(post)
	#write a row to the csv file
	frontReview.writerow(subArray)

def write_subscribe_row(time):
	subArray = []
	subArray.append(time)
	for sub in subredditArray:
		subArray.append(get_subscribers(sub))
	subscriberReview.writerow(subArray)

def write_active_row(time):
	subArray = []
	subArray.append(time)
	for sub in subredditArray:
		subArray.append(get_active_users(sub))
	activeReview.writerow(subArray)

#this function tests to see if our code is working in a small scale
def test_run():
	for x in range(0, 5):
		currentTime = strftime("%Y-%m-%d %H:%M", gmtime())
		write_front_page_row(currentTime)
		write_subscribe_row(currentTime)
		write_active_row(currentTime)
		#Delay 15 Minutes
		print "DING\n"
		time.sleep(900)

#runs this for about 3 days
gather_reddit_data(288)
