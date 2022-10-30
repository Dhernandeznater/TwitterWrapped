import requests
import constants
from requests.structures import CaseInsensitiveDict
import json
from postTweets import runWrappedForUser


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
        fullQuoteList += resp.json()['data']
        tracker += 1
        if 'next_token' in resp.json()['meta']:
            params['next_token'] = resp.json()['meta']['next_token']
        else:
            break

    return fullQuoteList

def getRetweets():
    url = f"{constants.TWEETS_ENDPOINT}/{constants.TWEET_URL_ID}/retweeted_by"
    # print(url)

    headers = CaseInsensitiveDict()
    headers["Authorization"] = constants.BEARER
    params = {"max_results": 100}
    fullUserList = []
    tracker = 0

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


def getProcessedAndPostedIDs():
    textfile = open(f"{constants.GENERAL_FILE_PATH}/posted.txt", "r")

    users = textfile.readlines()
    users = [user.strip() for user in users]
    return users


userList = getRetweets()
print(userList)
print(len(userList))