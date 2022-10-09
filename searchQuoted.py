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

def getProcessedAndPostedIDs():
    textfile = open(f"{constants.GENERAL_FILE_PATH}/posted.txt", "r")

    users = textfile.readlines()
    users = [user.strip() for user in users]
    return users

quoteList = getAllQuotes()
postedIDs = getProcessedAndPostedIDs()

filteredQuoteList = [tweet for tweet in quoteList if tweet['author_id'] not in postedIDs]

print(filteredQuoteList)

# list = ['dhernandeznater', 'fedehn', 'antolmos28']

# runWrappedForUser("NaterCarmen")

# for username in list:
#     print(f"Running for user {username}")
#     runWrappedForUser(username)

