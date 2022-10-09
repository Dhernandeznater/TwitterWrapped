from time import sleep
import postTweets, pullTweets, constants, wrappedCards



username = input("Enter username: ")

print(f"Grabbing and Compiling Tweets for {username}")
tweetCounter, totalLikes, totalComments, totalRetweets, mostLikedTweet, mostCommentedTweet, mostRetweetedTweet, amtOver5, amtOver10, amtOver20 = pullTweets.getAndCompileTweets(username)

print("Creating Cards")
wrappedCards.createMainStatsImage(totalLikes, totalComments, totalRetweets, username)
wrappedCards.createAmtLikesImage(amtOver5, amtOver10, amtOver20, username)
wrappedCards.createWordCloud(username)