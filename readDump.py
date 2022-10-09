import requests
from requests.structures import CaseInsensitiveDict
import json


def compileTweetData(username):
    with open(f'/Users/dhernandeznater/Desktop/{username}.txt', 'r') as f:
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

    print(f"Total Amount of Tweets: {tweetCounter}")
    print(f"Total Amount of Likes: {totalLikes}")
    print(f"Total Amount of Comments: {totalComments}")
    print(f"Total Times Retweeted: {totalRetweets}")
    print(f"Most liked tweet: {mostLikedTweet['text']}, {mostLikedCounter} likes")
    print(f"Most commented tweet: {mostCommentedTweet['text']}, {mostCommentedCount} comments")
    print(f"most Retweeted Tweet: {mostRetweetedTweet['text']}, {mostRetweetedCounter} retweets")
