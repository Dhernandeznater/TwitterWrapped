import os
import constants
import tweepy
import requests
from requests.structures import CaseInsensitiveDict
import json
from wrappedCards import runWrappedForUser

# Uses the tweepy api to upload all 3 wrapped pics and tweet them as a reply to quoteID.
# In addition, it replies to the newly uploaded tweet with a reference to a user's most liked tweet
# Finally, it updates the posted.txt file with the current username
def postWrappedReply(quoteID, username, id, mostLikedID, mostRetweetedID):
    auth = tweepy.OAuthHandler(constants.API_KEY, constants.API_SECRET_KEY)
    auth.set_access_token(constants.ACCESS_TOKEN, constants.ACCESS_SECRET_TOKEN)

    client = tweepy.Client(bearer_token=constants.BEARER_ONLY, consumer_key=constants.API_KEY, consumer_secret=constants.API_SECRET_KEY, 
                        access_token=constants.ACCESS_TOKEN, access_token_secret=constants.ACCESS_SECRET_TOKEN)


    auth1_1 = tweepy.OAuthHandler(constants.API_KEY, constants.API_SECRET_KEY).set_access_token(constants.ACCESS_TOKEN, constants.ACCESS_SECRET_TOKEN)
    api1_1 = tweepy.API(auth)
    print("Uploading First Pic")
    main_stats = api1_1.media_upload(f"{constants.GENERAL_FILE_PATH}/{username}/{username}_MainStats.jpg")
    print("Uploading Second Pic")
    like_stats = api1_1.media_upload(f"{constants.GENERAL_FILE_PATH}/{username}/{username}_LikeStats.jpg")
    print("Uploading Third Pic")
    word_cloud = api1_1.media_upload(f"{constants.GENERAL_FILE_PATH}/{username}/{username}_WordCloud.jpg")

    print("Posting First Tweet")
    wrappedPhotos = client.create_tweet(media_ids=[main_stats.media_id, like_stats.media_id, word_cloud.media_id], in_reply_to_tweet_id=quoteID)
    print("Posting Second Tweet")
    mostLiked = client.create_tweet(text="Your Most Liked Tweet:", in_reply_to_tweet_id=wrappedPhotos[0]['id'], quote_tweet_id=mostLikedID)
    print("Posting Third Tweet")
    client.create_tweet(text="Your Most Retweeted Tweet:", in_reply_to_tweet_id=mostLiked[0]['id'], quote_tweet_id=mostRetweetedID)

    textfile = open(f"{constants.GENERAL_FILE_PATH}/posted.txt", "a")
    textfile.write(id + "\n")
    textfile.close()

def postWrappedStandalone(username, id, mostLikedTweet, mostRetweetedTweet):
    auth = tweepy.OAuthHandler(constants.API_KEY, constants.API_SECRET_KEY)
    auth.set_access_token(constants.ACCESS_TOKEN, constants.ACCESS_SECRET_TOKEN)

    client = tweepy.Client(bearer_token=constants.BEARER_ONLY, consumer_key=constants.API_KEY, consumer_secret=constants.API_SECRET_KEY, 
                        access_token=constants.ACCESS_TOKEN, access_token_secret=constants.ACCESS_SECRET_TOKEN)


    api1_1 = tweepy.API(auth)
    print("Uploading First Pic")
    main_stats = api1_1.media_upload(f"{constants.GENERAL_FILE_PATH}/{username}/{username}_MainStats.jpg")
    print("Uploading Second Pic")
    like_stats = api1_1.media_upload(f"{constants.GENERAL_FILE_PATH}/{username}/{username}_LikeStats.jpg")
    print("Uploading Third Pic")
    year_over_year = api1_1.media_upload(f"{constants.GENERAL_FILE_PATH}/{username}/{username}_YearOverYear.jpg")
    print("Uploading Fourth Pic")
    word_cloud = api1_1.media_upload(f"{constants.GENERAL_FILE_PATH}/{username}/{username}_WordCloud.jpg")

    print("Posting First Tweet")
    tweetText = f"@{username} {constants.TWEET_TEXT}"
    wrappedPhotos = client.create_tweet(text=tweetText, media_ids=[main_stats.media_id, like_stats.media_id, year_over_year.media_id, word_cloud.media_id])
    print("Posting Second Tweet")
    if 'id' in mostLikedTweet:
        mostLiked = client.create_tweet(text="Your Most Liked Tweet:", in_reply_to_tweet_id=wrappedPhotos[0]['id'], quote_tweet_id=mostLikedTweet['id'])
        print("Posting Third Tweet")
        if 'id' in mostRetweetedTweet:
            client.create_tweet(text="Your Most Retweeted Tweet:", in_reply_to_tweet_id=mostLiked[0]['id'], quote_tweet_id=mostRetweetedTweet['id'])

    textfile = open(f"{constants.GENERAL_FILE_PATH}/posted.txt", "a")
    textfile.write(id + "\n")
    textfile.close()

def getAllQuotes():
    url = f"{constants.RECENT_TWEET_SEARCH}"

    headers = CaseInsensitiveDict()
    headers["Authorization"] = constants.BEARER
    params = {"query" : f'url:"{constants.TWEET_URL}" is:quote', "tweet.fields": "in_reply_to_user_id,author_id,conversation_id,attachments", "max_results": 100}

    fullQuoteList = []
    print(f"------------------ Gathering Quote Tweets ------------------")
    tracker = 0
    while True:
        print(f"Request Number {tracker}")
        resp = requests.get(url, headers=headers, params=params)
        if "data" in resp.json():
            fullQuoteList += resp.json()['data']
        tracker += 1
        if 'next_token' in resp.json()['meta']:
            params['next_token'] = resp.json()['meta']['next_token']
        else:
            break

    return fullQuoteList

def getRetweets():
    url = f"{constants.TWEETS_ENDPOINT}/{constants.TWEET_URL_ID}/retweeted_by"

    headers = CaseInsensitiveDict()
    headers["Authorization"] = constants.BEARER
    params = {"max_results": 100}
    fullUserList = []
    tracker = 0
    print(f"------------------ Gathering Retweets ------------------")

    while True:
        print(f"Request Number {tracker}")
        resp = requests.get(url, headers=headers, params=params)
        if 'data' in resp.json():
            fullUserList += resp.json()['data']
        tracker += 1
        if 'meta' in resp.json() and 'next_token' in resp.json()['meta']:
            params['pagination_token'] = resp.json()['meta']['next_token']
        else:
            break
        
    return fullUserList

def getPostedIDs():
    textfile = open(f"{constants.GENERAL_FILE_PATH}/posted.txt", "r")

    users = textfile.readlines()
    users = [user.strip() for user in users]
    return users
    


