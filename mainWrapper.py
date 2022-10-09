from time import sleep
import postTweets, pullTweets, constants, wrappedCards


while (True):

    # Get and filter quote tweets
    quotes = postTweets.getAllQuotes()
    postedIDs = postTweets.getPostedIDs()

    filteredQuoteList = [tweet for tweet in quotes if tweet['author_id'] not in postedIDs]



    for quote in filteredQuoteList:
        username = pullTweets.getUsernameFromID(quote['author_id'])

        print(f"Grabbing and Compiling Tweets for {username}")
        tweetCounter, totalLikes, totalComments, totalRetweets, mostLikedTweet, mostCommentedTweet, mostRetweetedTweet, amtOver5, amtOver10, amtOver20 = pullTweets.getAndCompileTweets(username)

        print("Creating Cards")
        wrappedCards.createMainStatsImage(totalLikes, totalComments, totalRetweets, username)
        wrappedCards.createAmtLikesImage(amtOver5, amtOver10, amtOver20, username)
        wrappedCards.createWordCloud(username)

        print("Posting Tweets")
        postTweets.postWrapped(quote["id"], username, quote['author_id'], mostLikedTweet["id"], mostRetweetedTweet["id"])

    print("Going to sleep for 5 minutes. If you want to stop the bot do it now.")
    sleep(1800)