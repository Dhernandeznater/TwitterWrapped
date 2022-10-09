import pullTweets
import requests
import constants
from requests.structures import CaseInsensitiveDict
import json
import os
import datetime
from dateutil import parser
import pytz


print(pullTweets.getIDFromUserName("dhernandeznater"))

def requestWithPaginations(url, params={}):
    headers = CaseInsensitiveDict()
    headers["Authorization"] = constants.BEARER
    print(params)
    fullData = []
    tracker = 0
    hasToken = True 

    while hasToken:
        print("Request Number {}".format(tracker))
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code != 200:
            print("Something went wrong, status code: {}".format(resp.status_code))
            print(resp)
            return []
        fullData += resp.json()['data']
        tracker += 1
        if 'next_token' in resp.json()['meta']:
            params['pagination_token'] = resp.json()['meta']['next_token']
        else:
            hasToken = False
    return fullData 

def getFollowers(id):
    url = f"https://api.twitter.com/2/users/{id}/followers"
    print("Getting Followers")
    return requestWithPaginations(url)

def getFollowing(id):
    url = f"https://api.twitter.com/2/users/{id}/following"
    print("Getting Following")
    return requestWithPaginations(url)

def getLiked(id):
    url = f"https://api.twitter.com/2/users/{id}/liked_tweets"
    print("Getting liked tweets")
    headers = CaseInsensitiveDict()
    headers["Authorization"] = constants.BEARER
    params = {'tweet.fields':'created_at'}
    fullData = []
    tracker = 0
    hasToken = True 

    while hasToken:
        print("Request Number {}".format(tracker))
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code != 200:
            print("Something went wrong, status code: {}".format(resp.status_code))
            print(resp)
            return []
        fullData += resp.json()['data']
        tracker += 1
        if 'next_token' in resp.json()['meta']:
            params['pagination_token'] = resp.json()['meta']['next_token']
        else:
            hasToken = False

        if parser.parse(resp.json()['data'][len(resp.json()['data']) - 1]['created_at']) < parser.parse('2022-01-01T00:00:00Z'):
            break

    return fullData 

def getTweets(id):
    url = f"https://api.twitter.com/2/users/{id}/tweets"
    params = {}
    params['start_time'] = '2022-01-01T00:00:00Z'
    params['max_results'] = 100
    recentTweets = requestWithPaginations(url, params)

    print(len(recentTweets))

    with open("recentTweets.txt", 'w') as f:
        json.dump(recentTweets, f)



id = pullTweets.getIDFromUserName("dhernandeznater")
# followers = getFollowers(id)
# following = getFollowing(id)

# print(len(followers))
# print(len(following))

# mutuals = [profile for profile in followers if profile in following]

# print((mutuals))

getTweets(id)


