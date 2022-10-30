class WrappedData:
    def __init__(self, tweetCounter = 0, totalLikes = 0, totalComments = 0, totalRetweets = 0, mostLikedTweet = {},
    mostCommentedTweet = {}, mostRetweetedTweet = {}, amtOver5 = 0, amtOver10 = 0, amtOver20 = 0):
        self.tweetCounter = tweetCounter
        self.totalLikes = totalLikes
        self.totalComments = totalComments
        self.totalRetweets = totalRetweets
        self.mostLikedTweet = mostLikedTweet
        self.mostCommentedTweet = mostCommentedTweet
        self.mostRetweetedTweet = mostRetweetedTweet
        self.amtOver5 = amtOver5
        self.amtOver10 = amtOver10
        self.amtOver20 = amtOver20

    def compareStats(self, otherWrappedData):
        return self.tweetCounter - otherWrappedData.tweetCounter, self.totalLikes - otherWrappedData.totalLikes, self.totalComments - otherWrappedData.totalComments, self.totalRetweets - otherWrappedData.totalRetweets 