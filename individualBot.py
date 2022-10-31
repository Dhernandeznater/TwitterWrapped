from asyncio import constants
from time import sleep
import pullTweets, wrappedCards, constants



username = input("Enter username: ")

print(f"Grabbing and Compiling Tweets for {username}")
userData21 = pullTweets.getAndCompileTweets(username, constants.START_DATE_2021, constants.END_DATE_2021)
userData22 = pullTweets.getAndCompileTweets(username, constants.START_DATE_2022, constants.END_DATE_2022)

print("Creating Cards")
wrappedCards.createMainStatsImage(userData22, username)
wrappedCards.createAmtLikesImage(userData22.amtOver5, userData22.amtOver10, userData22.amtOver20, username)
wrappedCards.createWordCloud(username, constants.START_DATE_2022[:4])
wrappedCards.createYearComparisonImage(userData21, userData22, username)