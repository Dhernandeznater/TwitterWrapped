import requests
import constants
from requests.structures import CaseInsensitiveDict
import wordcloud
from wordcloud import WordCloud, STOPWORDS
import numpy as np
import matplotlib.pyplot as plt
import json
import os
import re

def createWordCloud(username):
    with open(f'/Users/dhernandeznater/Desktop/TweetData/dhernandeznater.txt', 'r') as f:
            stringData = f.read()
            data = json.loads(stringData)

    year_text = ""

    for tweet in data:
        year_text += " " + tweet['text']

    year_text = re.sub(r"(http\S+)|(@\S+)|(\S+’\S+)", '', year_text, flags=re.MULTILINE).lower()

    stopwords = set(STOPWORDS)
    userCloud = WordCloud(width=2048, height=2048, background_color="#025587", stopwords=stopwords, min_font_size=10, color_func=lambda *args, **kwargs: (43,240,255)).generate(year_text)
    userCloud.to_file(f"/Users/dhernandeznater/Desktop/TweetData/{username}_WordCloud.jpg")


# path = f"/Users/dhernandeznater/Desktop/TweetData/dhernandeznater"
# if os.path.isdir(path):
#     print("path found")
# else:
#     print("not found")
#     os.mkdir("/Users/dhernandeznater/Desktop/TweetData/dhernandeznater")

