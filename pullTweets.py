import requests
import constants
from requests.structures import CaseInsensitiveDict
from wrappedData import WrappedData
import json
import os



def getIDFromUserName(username):
    url = f"https://api.twitter.com/labs/2/users/by/username/{username}"
    headers = CaseInsensitiveDict()
    headers["Authorization"] = constants.BEARER

    resp = requests.get(url, headers=headers)

    if resp.status_code == 200 and 'data' in resp.json() and 'id' in resp.json()['data']:
        return resp.json()['data']['id']

    return f"Something went wrong, status code: {resp.status_code}"

def getUsernameFromID(id):
    url = f"https://api.twitter.com/2/users/{id}"
    headers = CaseInsensitiveDict()
    headers["Authorization"] = constants.BEARER

    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        return resp.json()['data']['username']

    return f"Something went wrong, status code: {resp.status_code}"


def getTweetsInInterval(userID, username, startTime, endTime):
    print(f"Gathering tweets for {username}")
    folder_path = f"{constants.GENERAL_FILE_PATH}/{username}"
    path = f"{constants.GENERAL_FILE_PATH}/{username}/{username}_{startTime[:4]}.txt"

    # Check if TweetData folder exists
    if not os.path.isdir("TweetData"):
        os.mkdir("TweetData")

    # Make folder for individual user and check if there's a cached file
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)
    if os.path.isfile(path):
        print(f"Cached file for {username} found")
        return


    url = f"https://api.twitter.com/2/users/{userID}/tweets"

    headers = CaseInsensitiveDict()
    headers["Authorization"] = constants.BEARER
    params = {'start_time': f'{startTime}', 'end_time': f'{endTime}', 'max_results': 100, 'tweet.fields':'public_metrics', 'exclude':'retweets'}

    fullTweetList = []
    tracker = 0
    # Loop through and get all tweet data
    while True:
        print(f"Request Number {tracker}...")
        resp = requests.get(url, headers=headers, params=params)
        if ('data' in resp.json()) :
            fullTweetList += resp.json()['data']
        tracker += 1
        if 'meta' in resp.json() and 'next_token' in resp.json()['meta']:
            params['pagination_token'] = resp.json()['meta']['next_token']
        else:
            break

    with open(path, 'w') as f:
        json.dump(fullTweetList, f)


def compileTweetData(username, startTime):
    with open(f'{constants.GENERAL_FILE_PATH}/{username}/{username}_{startTime[:4]}.txt', 'r') as f:
        print('------------------ Twitter Stats ------------------')
        stringData = f.read()
        data = json.loads(stringData)

    tweetCounter = 0
    totalLikes = 0
    totalComments = 0
    totalRetweets = 0
    mostLikedCounter = 0
    mostCommentedCount = 0
    mostRetweetedCounter = 0
    mostLikedTweet = {}
    mostCommentedTweet = {}
    mostRetweetedTweet = {}
    amtOver5 = 0
    amtOver10 = 0
    amtOver20 = 0

    for tweet in data:
        
        # Update all trackers
        tweetCounter += 1
        public_metrics = tweet['public_metrics']
        totalLikes += public_metrics['like_count']
        totalComments += public_metrics['reply_count']
        totalRetweets += public_metrics['retweet_count']

        if public_metrics['reply_count'] > mostCommentedCount:
            mostCommentedCount = public_metrics['reply_count']
            mostCommentedTweet = tweet

        if public_metrics['like_count'] > mostLikedCounter:
            mostLikedCounter = public_metrics['like_count']
            mostLikedTweet = tweet

        if public_metrics['retweet_count'] > mostRetweetedCounter:
            mostRetweetedCounter = public_metrics['retweet_count']
            mostRetweetedTweet = tweet

        if public_metrics['like_count'] >= 5:
            amtOver5 += 1
            if public_metrics['like_count'] >= 10:
                amtOver10 += 1
                if public_metrics['like_count'] >= 20:
                    amtOver20 += 1

    print(f"Total Amount of Tweets: {tweetCounter}")
    print(f"Total Amount of Likes: {totalLikes}")
    print(f"Total Amount of Comments: {totalComments}")
    print(f"Total Times Retweeted: {totalRetweets}")
    if "text" in mostLikedTweet and "text" in mostCommentedTweet and "text" in mostRetweetedTweet:
        print(f"Most liked tweet: {mostLikedTweet['text']}, {mostLikedCounter} likes")
        print(f"Most commented tweet: {mostCommentedTweet['text']}, {mostCommentedCount} comments")
        print(f"most Retweeted Tweet: {mostRetweetedTweet['text']}, {mostRetweetedCounter} retweets")
    print(f"You had {amtOver5} Tweets get at least 5 likes")
    print(f"You had {amtOver10} Tweets get at least 10 likes")
    print(f"You had {amtOver20} Tweets get at least 20 likes")

    userData = WrappedData(tweetCounter, totalLikes, totalComments, totalRetweets, mostLikedTweet,
     mostCommentedTweet, mostRetweetedTweet, amtOver5, amtOver10, amtOver20)

    return userData

def getAndCompileTweets(username, startTime, endTime):
    userID = getIDFromUserName(username)

    getTweetsInInterval(userID, username, startTime, endTime)
    return compileTweetData(username, startTime)




