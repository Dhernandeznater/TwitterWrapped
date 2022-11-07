from time import sleep
import postTweets, pullTweets, constants, wrappedCards


while (True):

    # Get and filter quote tweets
    # quotes = postTweets.getAllQuotes()
    retweets = postTweets.getRetweets()
    postedIDs = postTweets.getPostedIDs()

    # filteredQuoteList = [tweet for tweet in quotes if tweet['author_id'] not in postedIDs]
    filteredUserList = [user for user in retweets if user['id'] not in postedIDs]


    for user in filteredUserList:
        username = user['username']
        userId = user['id']
        # Get and compile tweet data 2022
        print(f"Grabbing and Compiling Tweets for {username} for 2021")
        userData2021 = pullTweets.getAndCompileTweets(username, constants.START_DATE_2021, constants.END_DATE_2021)
        print(f"Grabbing and Compiling Tweets for {username} for 2022")
        userData2022 = pullTweets.getAndCompileTweets(username, constants.START_DATE_2022, constants.END_DATE_2022)

        print("Creating Cards")
        wrappedCards.createMainStatsImage(userData2022, username)
        wrappedCards.createAmtLikesImage(userData2022.amtOver5, userData2022.amtOver10, userData2022.amtOver20, username)
        wrappedCards.createWordCloud(username, constants.START_DATE_2022[:4])
        wrappedCards.createYearComparisonImage(userData2021, userData2022, username)

        print("Posting Tweets")
        postTweets.postWrappedStandalone(username, userId, userData2022.mostLikedTweet, userData2022.mostRetweetedTweet)

    print("Going to sleep for 5 minutes. If you want to stop the bot do it now.")
    sleep(1800)