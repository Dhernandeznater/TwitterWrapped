from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from pullTweets import getAndCompileTweets
import constants
import random
import json
import wrappedData
import re
import wordcloud
from wordcloud import WordCloud, STOPWORDS

# Creates the main stats image with total likes comments and retweets
def createMainStatsImage(userData, username):
    # Declare Variables
    image = Image.open("blueTemplate.jpg")
    image_editable = ImageDraw.Draw(image)

    # Create Title Text
    title_text = "Your 2022 Main Stats:"
    text_width, text_height = image_editable.textsize(title_text, font=constants.FONT)
    image_editable.text(((constants.IM_WIDTH - text_width) / 2, 80), title_text, constants.DARK_BLUE, font=constants.FONT)

    # Create Body Text
    main_text = [f"{userData.tweetCounter} Total Tweets", f"{userData.totalLikes} Total Likes", 
        f"{userData.totalRetweets} Retweets", f"{userData.totalComments} Comments"]

    for i, line in enumerate(main_text):
        width, height = image_editable.textsize(line, font=constants.FONT)
        line_height = 450 + (i * constants.LINE_SPACE_FOUR)

        image_editable.text(((constants.IM_WIDTH - width) / 2, line_height), line, constants.LIGHT_BLUE, 
                            font=constants.FONT, stroke_width=4, stroke_fill=constants.WHITE)

    # Add Watermark
    image_editable.text((1388, 1948), constants.WATERMARK, constants.LIGHT_BLUE, 
                        font=constants.WATERMARK_FONT, stroke_width=0, stroke_fill=constants.WHITE)

    # Brighten and Save Image
    enhancer = ImageEnhance.Brightness(image)
    im_output = enhancer.enhance(1.5)
    im_output.save(f"{constants.GENERAL_FILE_PATH}/{username}/{username}_MainStats.jpg")

def moreOrLess(stat, statName):
    return f"{abs(stat)} {'less' if stat < 0 else 'more'} {statName}"

def createYearComparisonImage(userDataPrevious, userDataCurrent, username):
    image = Image.open("blueTemplate.jpg")
    image_editable = ImageDraw.Draw(image)

    # Create Title Text
    title_text = "In 2022, you had"
    text_width, text_height = image_editable.textsize(title_text, font=constants.FONT)
    image_editable.text(((constants.IM_WIDTH - text_width) / 2, 80), title_text, constants.DARK_BLUE, font=constants.FONT)

    # Create Body Text
    tweetDif, likeDif, commentDif, retweetDif = userDataCurrent.compareStats(userDataPrevious)
    main_text = [moreOrLess(tweetDif, "tweets"), moreOrLess(likeDif, "likes"), moreOrLess(commentDif, "comments"), moreOrLess(retweetDif, "retweets")]
    for i, line in enumerate(main_text):
        width, height = image_editable.textsize(line, font=constants.FONT)
        line_height = 450 + (i * constants.LINE_SPACE_FOUR)

        image_editable.text(((constants.IM_WIDTH - width) / 2, line_height), line, constants.LIGHT_BLUE, 
                            font=constants.FONT, stroke_width=4, stroke_fill=constants.WHITE)

    # Add Watermark
    image_editable.text((1388, 1948), constants.WATERMARK, constants.LIGHT_BLUE, 
                        font=constants.WATERMARK_FONT, stroke_width=0, stroke_fill=constants.WHITE)

    # Brighten and Save Image
    enhancer = ImageEnhance.Brightness(image)
    im_output = enhancer.enhance(1.5)
    im_output.save(f"{constants.GENERAL_FILE_PATH}/{username}/{username}_YearOverYear.jpg")
    

def createAmtLikesImage(amtOver5, amtOver10, amtOver20, username):
    # Declare Constants
    image = Image.open("blueTemplate.jpg")
    image_editable = ImageDraw.Draw(image)

    # Create Title Text
    title_texts = ["Someone's Popular!", "Raking in the Likes!", "Heck Yeah!", "Putting up Numbers!", "Go Off!!", "The Bangers:"]
    chosen_text = random.choice(title_texts)
    if username in constants.CUSTOM_TITLES.keys():
        chosen_text = constants.CUSTOM_TITLES[username]
    text_width, text_height = image_editable.textsize(chosen_text, font=constants.FONT)
    image_editable.text(((constants.IM_WIDTH - text_width) / 2, 80), chosen_text, constants.DARK_BLUE, font=constants.FONT)

    # Create Body Text
    body_font = ImageFont.truetype('SF-Pro-Rounded-Heavy.ttf', 150)
    main_texts = [f"{amtOver5} Tweets >= 5 Likes", f"{amtOver10} Tweets >= 10 Likes", f"{amtOver20} Tweets >= 20 Likes"]
    for i, line in enumerate(main_texts):
        width, height = image_editable.textsize(line, font=body_font)
        line_height = 350 + 200 + (i * constants.LINE_SPACE)

        image_editable.text(((constants.IM_WIDTH - width) / 2, line_height), line, constants.LIGHT_BLUE,
                            font=body_font, stroke_width=4, stroke_fill=constants.WHITE)

    # Add Watermark
    image_editable.text((1388, 1948), constants.WATERMARK, constants.LIGHT_BLUE, 
                        font=constants.WATERMARK_FONT, stroke_width=0, stroke_fill=constants.WHITE)

    # Brighten and Save Image
    enhancer = ImageEnhance.Brightness(image)
    im_output = enhancer.enhance(1.5)
    im_output.save(f"{constants.GENERAL_FILE_PATH}/{username}/{username}_LikeStats.jpg")
    

def createWordCloud(username, year):
    # Read Tweet Data
    with open(f'{constants.GENERAL_FILE_PATH}/{username}/{username}_{year}.txt', 'r') as f:
            stringData = f.read()
            data = json.loads(stringData)

    # Filter Text
    year_text = ""
    for tweet in data:
        year_text += " " + tweet['text']
    year_text = re.sub(r"(http\S+)|(@\S+)|(\S+’\S+)", '', year_text, flags=re.MULTILINE).lower()
    
    if year_text == "":
        year_text = "Tweet more or get off private!"

    # Create Wordcloud
    stopwords = set(STOPWORDS.union({'gt'}))
    userCloud = WordCloud(width=2048, height=2048, background_color="#025587", stopwords=stopwords, min_font_size=10, color_func=lambda *args, **kwargs: (43,240,255)).generate(year_text)
    userCloud.to_file(f"{constants.GENERAL_FILE_PATH}/{username}/{username}_WordCloud.jpg")


def runWrappedForUser(user):
    userData = getAndCompileTweets(user)
    print("Creating Main Stats Image")
    createMainStatsImage(userData.totalLikes, userData.totalComments, userData.totalRetweets, user)
    print("Create Amount Likes Image")
    createAmtLikesImage(userData.amtOver5, userData.amtOver10, userData.amtOver20, user)
    print("Creating Word Cloud")
    createWordCloud(user)

